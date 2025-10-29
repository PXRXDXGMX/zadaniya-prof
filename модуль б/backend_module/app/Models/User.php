<?php

namespace App\Models;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class User extends Authenticatable {
    use HasFactory;
    protected $fillable = ['nickname','email','password','token'];
    protected $hidden = ['password'];
    public function posts(){ return $this->hasMany(Post::class); }
    public function likes(){ return $this->hasMany(Like::class); }
}
