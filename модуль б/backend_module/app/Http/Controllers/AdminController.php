<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class AdminController extends Controller
{
    public function login (Request $request) {
        $validator = validator($request->all(), [
            'email' => 'required',
            'password' => 'required'
        ]);

        if ($validator->fails()) return back()->withErrors($validator->errors())->withInput();

        if(!auth()->attempt($validator->validated())) return back()->withErrors(['error' => 'Не верные данные'])->withInput();

        $user = auth()->user();

        if($user->role !== 'admin') {
            auth()->logout();
            return back()->withErrors(['error' => 'Вы не админ']);
        }

        return back();
    }

    public function admin (Request $request) {
        $user = auth()->user();

        if($user && $user->role === 'admin')
        {
            $allUsers = User::query()->where('role', 'user')->get();
            $users = User::query()->where('nickname', 'like', '%' . $request->nickname . '%')->where('role', 'user')->get();

            return view('users', compact('users', 'allUsers'));
        }

        return view('login');
    }
    public function logout() {
        auth()->logout();
        return back();
    }
    public function toggleStatus(Request $request, User $user) {
        $newStatus = $user->status === 'active' ? 'banned' : 'active';

        $user->update(['status' => $newStatus]);

        return back();
    }
}
