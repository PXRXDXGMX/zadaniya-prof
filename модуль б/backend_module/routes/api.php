<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\PostController;
use App\Http\Controllers\UserController;

Route::post('/api-of/register',[AuthController::class,'register']);
Route::post('/api-of/login',[AuthController::class,'login']);
Route::get('/api-of/logout',[AuthController::class,'logout']);

Route::get('/api-of/posts',[PostController::class,'index']);
Route::post('/api-of/posts',[PostController::class,'store']);
Route::patch('/api-of/posts/{post}',[PostController::class,'update']);
Route::delete('/api-of/posts/{post}',[PostController::class,'destroy']);
Route::post('/api-of/posts/{post}/like',[PostController::class,'like']);
Route::delete('/api-of/posts/{post}/like',[PostController::class,'unlike']);

Route::get('/api-of/user/{id}',[UserController::class,'show']);
