<?php
// Test fixture containing intentional vulnerable PHP (Laravel, CodeIgniter) patterns

// 1. Insecure Deserialization
$data = unserialize($_POST['user_payload']);

// 2. SQL Injection in whereRaw
$users = DB::table('users')->whereRaw("email = '" . $request->input('email') . "'");

// 3. Mass assignment vulnerability
class User extends Model {
    protected $guarded = [];
}

// 4. Raw Blade XSS
// {!! $user->profile_bio !!}

// 5. CodeIgniter raw query concatenation
$ci_query = $this->db->query("SELECT * FROM items WHERE id = " . $item_id);

// 6. CodeIgniter CSRF disabled
$config['csrf_protection'] = FALSE;
