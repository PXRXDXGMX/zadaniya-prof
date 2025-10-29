<?php
namespace App\Http\Controllers;
use Illuminate\Http\Request;
use App\Models\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;

class AuthController extends Controller {

    public function register(Request $r) {
        $v = Validator::make($r->all(), [
            'nickname'=>'required|string|max:20|unique:users,nickname',
            'email'=>'required|email|unique:users,email',
            'password'=>'required|string|min:3'
        ]);
        if($v->fails()) return response()->json(["message"=>"Validation errors","errors"=>$v->errors()],422);

        $user = User::create([
            'nickname'=>$r->nickname,
            'email'=>$r->email,
            'password'=>bcrypt($r->password)
        ]);

        return response()->json(['data'=>['user'=>['nickname'=>$user->nickname,'email'=>$user->email]]],201);
    }

    public function login(Request $r) {
        $v = Validator::make($r->all(), ['email'=>'required|email','password'=>'required|string']);
        if($v->fails()) return response()->json(["message"=>"Validation errors","errors"=>$v->errors()],422);

        $user = User::where('email',$r->email)->first();
        if(!$user || !Hash::check($r->password,$user->password)) return response()->json(['message'=>'failed'],401);
        if($user->is_banned) return response()->json(['message'=>'User has been banned'],404);

        $token = bin2hex(random_bytes(16));
        $user->update(['token'=>$token]);

        return response()->json(['credentials'=>['token'=>$token]],200);
    }

    public function logout(Request $r) {
        $token = $r->header('Authorization');
        if(!$token) return response()->json(['message'=>'No token'],401);
        $token = str_replace('Bearer ','',$token);
        $user = User::where('token',$token)->first();
        if(!$user) return response()->json(['message'=>'Invalid token'],401);
        $user->update(['token'=>null]);
        return response()->json(null,204);
    }
}
