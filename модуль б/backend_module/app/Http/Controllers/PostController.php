<?php

namespace App\Http\Controllers;
use Illuminate\Http\Request;
use App\Models\Post;
use App\Models\User;
use App\Models\Like;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller {

    private function authUser($r){
        $token = $r->header('Authorization');
        if(!$token) return null;
        $token = str_replace('Bearer ','',$token);
        return User::where('token',$token)->first();
    }

    public function index(Request $r){
        $search = $r->query('search');
        $q = Post::with('user')->whereHas('user',fn($u)=>$u->where('is_banned',false));
        if($search) $q->where('title','like',"%$search%");
        $posts = $q->orderBy('id','desc')->paginate(10);
        return response()->json(['data'=>$posts],200);
    }

    public function store(Request $r){
        $user = $this->authUser($r);
        if(!$user) return response()->json(['message'=>'Invalid token'],401);

        $v = Validator::make($r->all(),[
            'title'=>'required|min:3',
            'description'=>'nullable|min:10',
            'img'=>'nullable|mimes:jpg,jpeg,png|max:4608'
        ]);
        if($v->fails()) return response()->json(["message"=>"Validation errors","errors"=>$v->errors()],422);

        $path = null;
        if($r->hasFile('img')) $path = $r->file('img')->store('posts','public');

        $post = Post::create([
            'user_id'=>$user->id,
            'title'=>$r->title,
            'description'=>$r->description,
            'img'=>$path
        ]);

        return response()->json(['data'=>$post],201);
    }

    public function update(Request $r, Post $post){
        $user = $this->authUser($r);
        if(!$user) return response()->json(['message'=>'Invalid token'],401);
        if($user->id!=$post->user_id) return response()->json(['message'=>'GET OUT!!','error_code'=>'4444'],403);

        $v = Validator::make($r->all(),[
            'title'=>'sometimes|min:3',
            'description'=>'sometimes|min:10',
            'img'=>'nullable|mimes:jpg,jpeg,png|max:4608'
        ]);
        if($v->fails()) return response()->json(["message"=>"Validation errors","errors"=>$v->errors()],422);

        if($r->hasFile('img')){
            if($post->img) Storage::disk('public')->delete($post->img);
            $post->img = $r->file('img')->store('posts','public');
        }
        if($r->title) $post->title=$r->title;
        if($r->description) $post->description=$r->description;
        $post->save();
        return response()->json(['data'=>$post],200);
    }

    public function destroy(Request $r, Post $post){
        $user = $this->authUser($r);
        if(!$user) return response()->json(['message'=>'Invalid token'],401);
        if($user->id!=$post->user_id) return response()->json(['message'=>'GET OUT!!','error_code'=>'4444'],403);
        if($post->img) Storage::disk('public')->delete($post->img);
        $post->delete();
        return response()->json(null,204);
    }

    public function like(Request $r, Post $post){
        $user = $this->authUser($r);
        if(!$user) return response()->json(['message'=>'Invalid token'],401);
        if(Like::where('user_id',$user->id)->where('post_id',$post->id)->exists())
            return response()->json(['error'=>['message'=>"There's already a like"]],403);
        Like::create(['user_id'=>$user->id,'post_id'=>$post->id]);
        return response()->json(['data'=>['message'=>'success']],201);
    }

    public function unlike(Request $r, Post $post){
        $user = $this->authUser($r);
        if(!$user) return response()->json(['message'=>'Invalid token'],401);
        $like = Like::where('user_id',$user->id)->where('post_id',$post->id)->first();
        if(!$like) return response()->json(['error'=>['message'=>'no likes']],403);
        $like->delete();
        return response()->json(['data'=>['message'=>'success']],200);
    }
}
