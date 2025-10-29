<?php

use App\Http\Controllers\AdminController;
use App\Http\Middleware\AdminCheck;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/admin', [AdminController::class, 'admin']);
Route::post('/login', [AdminController::class, 'login']);
Route::middleware(AdminCheck::class)->group(function() {
    Route::get('/logout', [AdminController::class, 'logout']);
    Route::patch('/users/{user}', [AdminController::class, 'toggleStatus']);



});
