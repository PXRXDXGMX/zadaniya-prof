<?php

namespace App\Http\Controllers;
use Illuminate\Http\Request;
use App\Models\User;

class UserController extends Controller {


    public function index(Request $request)
    {
        return ($request->all());
    }


    public function show($id){
        $user = User::find($id);
        if(!$user) return response()->json(['message'=>'Not Found'],404);
        if($user->is_banned) return response()->json(['message'=>'User has been banned'],404);
        if($user->role=='admin') return response()->json(['message'=>'Not Found'],404);

        $posts = $user->posts()->paginate(10);
        return response()->json(['data'=>['nickname'=>$user->nickname,'posts'=>$posts]],200);
    }
}
