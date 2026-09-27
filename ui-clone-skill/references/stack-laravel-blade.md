# Stack: Laravel Blade + Tailwind CSS

## Overview
Full-stack PHP framework with server-rendered Blade templates + Tailwind CSS (via Vite). Ideal for traditional web apps, admin panels, or SaaS with server-side rendering.

---

## Project Setup

```bash
composer create-project laravel/laravel project-name
cd project-name
npm install -D tailwindcss @tailwindcss/forms @tailwindcss/typography autoprefixer
npx tailwindcss init -p
npm install
```

### tailwind.config.js
```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './app/**/*.php',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary:   { DEFAULT: '#YOUR_PRIMARY', 50: '#...', 900: '#...' },
        surface:   '#YOUR_SURFACE',
      },
      fontFamily: {
        sans:    ['Inter', 'sans-serif'],
        heading: ['YOUR_HEADING_FONT', 'sans-serif'],
      },
      borderRadius: {
        card: '0.75rem',
      },
      boxShadow: {
        card: '0 4px 24px rgba(0,0,0,0.08)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

### resources/css/app.css
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --color-primary: #YOUR_PRIMARY;
    --color-surface: #YOUR_SURFACE;
    --color-text:    #YOUR_TEXT;
  }
  body { @apply font-sans text-gray-800 antialiased; }
  h1,h2,h3,h4,h5,h6 { @apply font-heading; }
}

@layer components {
  .btn-primary {
    @apply inline-flex items-center justify-center px-5 py-2.5 rounded-lg
           bg-primary text-white font-semibold text-sm
           hover:bg-primary/90 active:scale-95 transition-all duration-150;
  }
  .btn-secondary {
    @apply inline-flex items-center justify-center px-5 py-2.5 rounded-lg
           border border-gray-300 text-gray-700 font-semibold text-sm
           hover:bg-gray-50 active:scale-95 transition-all duration-150;
  }
  .card {
    @apply bg-white rounded-card shadow-card border border-gray-100 p-6;
  }
  .input {
    @apply w-full rounded-lg border-gray-300 text-sm
           focus:ring-primary focus:border-primary;
  }
}
```

### vite.config.js
```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
  plugins: [
    laravel({ input: ['resources/css/app.css', 'resources/js/app.js'], refresh: true }),
  ],
});
```

---

## Blade Layout Files

### resources/views/layouts/app.blade.php
```blade
<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" class="scroll-smooth">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="csrf-token" content="{{ csrf_token() }}" />
  <title>@yield('title', config('app.name'))</title>
  <meta name="description" content="@yield('description', 'Default description.')" />
  @vite(['resources/css/app.css', 'resources/js/app.js'])
  @stack('head')
</head>
<body class="bg-surface min-h-screen flex flex-col">
  @include('partials.navbar')
  <main class="flex-1">
    @yield('content')
  </main>
  @include('partials.footer')
  @stack('scripts')
</body>
</html>
```

### resources/views/layouts/auth.blade.php
```blade
<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>@yield('title', 'Auth') — {{ config('app.name') }}</title>
  @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
  @yield('content')
</body>
</html>
```

---

## Routes (routes/web.php)

```php
Route::get('/',              [HomeController::class,      'index'])->name('home');
Route::get('/about',         [PageController::class,      'about'])->name('about');
Route::get('/contact',       [PageController::class,      'contact'])->name('contact');
Route::get('/faq',           [PageController::class,      'faq'])->name('faq');
Route::get('/blog',          [BlogController::class,      'index'])->name('blog.index');
Route::get('/blog/{slug}',   [BlogController::class,      'show'])->name('blog.show');

Route::get('/login',         [AuthController::class,      'showLogin'])->name('login');
Route::post('/login',        [AuthController::class,      'login']);
Route::get('/register',      [AuthController::class,      'showRegister'])->name('register');
Route::post('/register',     [AuthController::class,      'register']);
Route::get('/forgot-password',[AuthController::class,     'showForgot'])->name('password.request');
Route::post('/forgot-password',[AuthController::class,    'sendResetLink'])->name('password.email');
Route::get('/reset-password/{token}',[AuthController::class,'showReset'])->name('password.reset');
Route::post('/reset-password',[AuthController::class,     'resetPassword'])->name('password.update');
Route::get('/otp',           [AuthController::class,      'showOtp'])->name('otp');

Route::prefix('legal')->name('legal.')->group(function () {
  Route::get('/',       [LegalController::class, 'index'])->name('index');
  Route::get('/privacy',[LegalController::class, 'privacy'])->name('privacy');
  Route::get('/terms',  [LegalController::class, 'terms'])->name('terms');
  Route::get('/refund', [LegalController::class, 'refund'])->name('refund');
});
```

---

## View Files Structure

```
resources/views/
├── layouts/
│   ├── app.blade.php
│   └── auth.blade.php
├── partials/
│   ├── navbar.blade.php
│   └── footer.blade.php
├── components/
│   ├── ui/
│   │   ├── button.blade.php
│   │   ├── card.blade.php
│   │   ├── badge.blade.php
│   │   └── input.blade.php
│   └── sections/
│       ├── hero.blade.php
│       ├── features.blade.php
│       └── cta.blade.php
├── pages/
│   ├── home.blade.php
│   ├── about.blade.php
│   ├── contact.blade.php
│   └── faq.blade.php
├── blog/
│   ├── index.blade.php
│   └── show.blade.php
├── auth/
│   ├── login.blade.php
│   ├── register.blade.php
│   ├── forgot-password.blade.php
│   ├── reset-password.blade.php
│   └── otp.blade.php
└── legal/
    ├── index.blade.php
    ├── privacy.blade.php
    ├── terms.blade.php
    └── refund.blade.php
```

---

## Blade Component Examples

### Anonymous Blade Component: Button
```blade
{{-- resources/views/components/ui/button.blade.php --}}
@props(['variant' => 'primary', 'size' => 'md', 'href' => null])
@php
  $base = 'inline-flex items-center justify-center font-semibold rounded-lg transition-all duration-150 active:scale-95';
  $variants = [
    'primary'   => 'bg-primary text-white hover:bg-primary/90',
    'secondary' => 'border border-gray-300 text-gray-700 hover:bg-gray-50',
    'ghost'     => 'text-primary hover:bg-primary/10',
  ];
  $sizes = ['sm' => 'px-3 py-1.5 text-sm', 'md' => 'px-5 py-2.5 text-sm', 'lg' => 'px-7 py-3 text-base'];
  $classes = "$base {$variants[$variant]} {$sizes[$size]}";
@endphp

@if($href)
  <a href="{{ $href }}" {{ $attributes->merge(['class' => $classes]) }}>{{ $slot }}</a>
@else
  <button {{ $attributes->merge(['class' => $classes, 'type' => 'button']) }}>{{ $slot }}</button>
@endif
```

Usage: `<x-ui.button variant="primary" href="/register">Get Started</x-ui.button>`

### Auth Login Page
```blade
{{-- resources/views/auth/login.blade.php --}}
@extends('layouts.auth')
@section('title', 'Sign In')
@section('content')
<div class="w-full max-w-md">
  <div class="bg-white rounded-2xl shadow-card p-8">
    <div class="text-center mb-8">
      <a href="/" class="text-2xl font-bold text-primary">BrandName</a>
      <h1 class="text-xl font-bold text-gray-900 mt-4">Sign in to your account</h1>
      <p class="text-gray-500 text-sm mt-1">Welcome back!</p>
    </div>

    @if ($errors->any())
      <div class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3 mb-6">
        {{ $errors->first() }}
      </div>
    @endif

    <form action="{{ route('login') }}" method="POST" class="space-y-4">
      @csrf
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input type="email" id="email" name="email" required autocomplete="email"
               value="{{ old('email') }}"
               class="input @error('email') border-red-400 @enderror"
               placeholder="you@example.com" />
        @error('email')<p class="text-red-500 text-xs mt-1">{{ $message }}</p>@enderror
      </div>
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
        <input type="password" id="password" name="password" required autocomplete="current-password"
               class="input @error('password') border-red-400 @enderror"
               placeholder="••••••••" />
        @error('password')<p class="text-red-500 text-xs mt-1">{{ $message }}</p>@enderror
      </div>
      <div class="flex items-center justify-between">
        <label class="flex items-center gap-2 text-sm text-gray-600">
          <input type="checkbox" name="remember" class="rounded border-gray-300 text-primary" />
          Remember me
        </label>
        <a href="{{ route('password.request') }}" class="text-sm text-primary hover:underline">Forgot password?</a>
      </div>
      <button type="submit" class="btn-primary w-full mt-2">Sign In</button>
    </form>

    <p class="text-center text-sm text-gray-500 mt-6">
      Don't have an account?
      <a href="{{ route('register') }}" class="text-primary font-medium hover:underline">Sign up</a>
    </p>
  </div>
</div>
@endsection
```

---

## Checklist

- [ ] Tailwind + Vite configured (`npm run dev`)
- [ ] `tailwind.config.js` content paths include `*.blade.php`
- [ ] `@tailwindcss/forms` plugin installed
- [ ] All routes defined in `routes/web.php`
- [ ] Layouts: `app.blade.php` and `auth.blade.php`
- [ ] Partials: `navbar.blade.php`, `footer.blade.php`
- [ ] Anonymous components in `resources/views/components/`
- [ ] All auth pages extend `layouts.auth`
- [ ] CSRF `@csrf` on all forms
- [ ] `@error` directives on all inputs
- [ ] All required pages/views created
