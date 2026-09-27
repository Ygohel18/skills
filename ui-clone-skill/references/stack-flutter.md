# Stack: Flutter (Cross-Platform)

## Overview
Google's cross-platform UI toolkit. Write once, deploy to iOS, Android, Web, and Desktop. Uses Dart with a widget-tree composition model and Material 3 / Cupertino theming.

---

## Project Setup

```bash
flutter create project_name --org com.example
cd project_name
flutter pub get
```

### pubspec.yaml dependencies
```yaml
name: project_name
description: A Flutter app.

environment:
  sdk: '>=3.3.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  # Navigation
  go_router: ^14.2.0
  # State management
  flutter_riverpod: ^2.5.1
  # UI / Utilities
  google_fonts: ^6.2.1
  cached_network_image: ^3.3.1
  flutter_svg: ^2.0.10+1
  # HTTP
  dio: ^5.5.0+1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/
    - assets/icons/
```

---

## Theme Setup (from DESIGN.md)

### lib/core/theme/app_colors.dart
```dart
import 'package:flutter/material.dart';

class AppColors {
  // Map DESIGN.md color tokens to Flutter Color objects
  static const primary         = Color(0xFF_YOUR_PRIMARY);    // e.g. 0xFF6366F1
  static const primaryLight    = Color(0xFF_YOUR_PRIMARY_LIGHT);
  static const secondary       = Color(0xFF_YOUR_SECONDARY);
  static const background      = Color(0xFF_YOUR_BG);
  static const surface         = Color(0xFF_YOUR_SURFACE);
  static const onPrimary       = Color(0xFFFFFFFF);
  static const onBackground    = Color(0xFF_YOUR_TEXT);
  static const onSurface       = Color(0xFF_YOUR_TEXT);
  static const textMuted       = Color(0xFF_YOUR_MUTED);
  static const border          = Color(0xFF_YOUR_BORDER);
  static const error           = Color(0xFFEF4444);
  static const success         = Color(0xFF22C55E);
  static const warning         = Color(0xFFF59E0B);

  // Dark mode
  static const backgroundDark  = Color(0xFF0F172A);
  static const surfaceDark     = Color(0xFF1E293B);
}
```

### lib/core/theme/app_theme.dart
```dart
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';

class AppTheme {
  static ThemeData get light => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.light(
      primary:         AppColors.primary,
      onPrimary:       AppColors.onPrimary,
      secondary:       AppColors.secondary,
      background:      AppColors.background,
      surface:         AppColors.surface,
      onBackground:    AppColors.onBackground,
      onSurface:       AppColors.onSurface,
      error:           AppColors.error,
    ),
    // Typography from DESIGN.md (replace Inter with your font)
    textTheme: GoogleFonts.interTextTheme().copyWith(
      displayLarge:  GoogleFonts.inter(fontSize: 57, fontWeight: FontWeight.bold),
      headlineLarge: GoogleFonts.inter(fontSize: 32, fontWeight: FontWeight.bold),
      headlineMedium:GoogleFonts.inter(fontSize: 24, fontWeight: FontWeight.w600),
      titleLarge:    GoogleFonts.inter(fontSize: 20, fontWeight: FontWeight.w600),
      bodyLarge:     GoogleFonts.inter(fontSize: 16),
      bodyMedium:    GoogleFonts.inter(fontSize: 14),
      labelLarge:    GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w600),
    ),
    // Card theme
    cardTheme: CardTheme(
      color: AppColors.surface,
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
    ),
    // Button theme
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.primary,
        foregroundColor: AppColors.onPrimary,
        minimumSize: const Size(double.infinity, 52),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        textStyle: GoogleFonts.inter(fontWeight: FontWeight.w600, fontSize: 16),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        minimumSize: const Size(double.infinity, 52),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        side: const BorderSide(color: AppColors.primary),
      ),
    ),
    // Input theme
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.border),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.primary, width: 2),
      ),
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
    ),
    appBarTheme: AppBarTheme(
      backgroundColor: AppColors.surface,
      elevation: 0,
      centerTitle: true,
      titleTextStyle: GoogleFonts.inter(
        fontSize: 18, fontWeight: FontWeight.w600, color: AppColors.onSurface,
      ),
    ),
  );

  static ThemeData get dark => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.dark(
      primary:      AppColors.primary,
      onPrimary:    AppColors.onPrimary,
      background:   AppColors.backgroundDark,
      surface:      AppColors.surfaceDark,
      onBackground: Colors.white,
      onSurface:    Colors.white,
    ),
    textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
  );
}
```

---

## Navigation (GoRouter)

### lib/core/router/app_router.dart
```dart
import 'package:go_router/go_router.dart';
import 'package:flutter/material.dart';
import '../../features/home/home_screen.dart';
import '../../features/auth/login_screen.dart';
import '../../features/auth/register_screen.dart';
import '../../features/auth/forgot_password_screen.dart';
import '../../features/auth/otp_screen.dart';
import '../../features/blog/blog_screen.dart';
import '../../features/blog/blog_detail_screen.dart';
import '../../features/about/about_screen.dart';
import '../../features/contact/contact_screen.dart';
import '../../features/legal/legal_screen.dart';
import '../../features/legal/legal_detail_screen.dart';
import '../widgets/scaffold_with_navbar.dart';

final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    ShellRoute(
      builder: (context, state, child) => ScaffoldWithNavBar(child: child),
      routes: [
        GoRoute(path: '/',       builder: (ctx, state) => const HomeScreen()),
        GoRoute(path: '/about',  builder: (ctx, state) => const AboutScreen()),
        GoRoute(path: '/contact',builder: (ctx, state) => const ContactScreen()),
        GoRoute(path: '/blog',   builder: (ctx, state) => const BlogScreen()),
        GoRoute(
          path: '/blog/:slug',
          builder: (ctx, state) => BlogDetailScreen(slug: state.pathParameters['slug']!),
        ),
      ],
    ),
    GoRoute(path: '/login',           builder: (ctx, state) => const LoginScreen()),
    GoRoute(path: '/register',        builder: (ctx, state) => const RegisterScreen()),
    GoRoute(path: '/forgot-password', builder: (ctx, state) => const ForgotPasswordScreen()),
    GoRoute(path: '/otp',             builder: (ctx, state) => const OtpScreen()),
    GoRoute(path: '/legal',           builder: (ctx, state) => const LegalScreen()),
    GoRoute(
      path: '/legal/:type',
      builder: (ctx, state) => LegalDetailScreen(type: state.pathParameters['type']!),
    ),
  ],
);
```

---

## File Structure

```
lib/
├── main.dart
├── core/
│   ├── theme/
│   │   ├── app_colors.dart
│   │   └── app_theme.dart
│   ├── router/
│   │   └── app_router.dart
│   └── widgets/
│       ├── scaffold_with_navbar.dart
│       ├── app_button.dart
│       ├── app_card.dart
│       └── app_text_field.dart
└── features/
    ├── home/
    │   └── home_screen.dart
    ├── auth/
    │   ├── login_screen.dart
    │   ├── register_screen.dart
    │   ├── forgot_password_screen.dart
    │   └── otp_screen.dart
    ├── blog/
    │   ├── blog_screen.dart
    │   └── blog_detail_screen.dart
    ├── about/
    │   └── about_screen.dart
    ├── contact/
    │   └── contact_screen.dart
    └── legal/
        ├── legal_screen.dart
        └── legal_detail_screen.dart
```

---

## Key Widget Patterns

### main.dart
```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/router/app_router.dart';
import 'core/theme/app_theme.dart';

void main() {
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'AppName',
      theme:      AppTheme.light,
      darkTheme:  AppTheme.dark,
      themeMode:  ThemeMode.system,
      routerConfig: appRouter,
      debugShowCheckedModeBanner: false,
    );
  }
}
```

### LoginScreen
```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey    = GlobalKey<FormState>();
  final _emailCtrl  = TextEditingController();
  final _passCtrl   = TextEditingController();
  bool _obscure     = true;
  bool _isLoading   = false;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      backgroundColor: theme.colorScheme.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const SizedBox(height: 48),
                Text('BrandName', style: theme.textTheme.headlineLarge?.copyWith(
                  color: theme.colorScheme.primary)),
                const SizedBox(height: 8),
                Text('Sign in to your account', style: theme.textTheme.titleLarge),
                const SizedBox(height: 40),
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      children: [
                        TextFormField(
                          controller: _emailCtrl,
                          keyboardType: TextInputType.emailAddress,
                          decoration: const InputDecoration(labelText: 'Email', hintText: 'you@example.com'),
                          validator: (v) => v!.contains('@') ? null : 'Enter a valid email',
                        ),
                        const SizedBox(height: 16),
                        TextFormField(
                          controller: _passCtrl,
                          obscureText: _obscure,
                          decoration: InputDecoration(
                            labelText: 'Password',
                            suffixIcon: IconButton(
                              icon: Icon(_obscure ? Icons.visibility_off : Icons.visibility),
                              onPressed: () => setState(() => _obscure = !_obscure),
                            ),
                          ),
                          validator: (v) => v!.length >= 6 ? null : 'Minimum 6 characters',
                        ),
                        Align(
                          alignment: Alignment.centerRight,
                          child: TextButton(
                            onPressed: () => context.push('/forgot-password'),
                            child: const Text('Forgot password?'),
                          ),
                        ),
                        const SizedBox(height: 8),
                        SizedBox(
                          width: double.infinity, height: 52,
                          child: ElevatedButton(
                            onPressed: _isLoading ? null : _submit,
                            child: _isLoading
                                ? const CircularProgressIndicator(color: Colors.white, strokeWidth: 2)
                                : const Text('Sign In'),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 24),
                Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  const Text("Don't have an account? "),
                  TextButton(
                    onPressed: () => context.push('/register'),
                    child: const Text('Sign up'),
                  ),
                ]),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);
    // TODO: Call auth provider
    await Future.delayed(const Duration(seconds: 1));
    setState(() => _isLoading = false);
    if (mounted) context.go('/');
  }

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passCtrl.dispose();
    super.dispose();
  }
}
```

---

## Checklist

- [ ] `pubspec.yaml` with `go_router`, `flutter_riverpod`, `google_fonts` dependencies
- [ ] `AppColors` with all DESIGN.md color tokens
- [ ] `AppTheme.light` and `AppTheme.dark` configured
- [ ] `GoRouter` with all routes including ShellRoute for BottomNavBar
- [ ] `MaterialApp.router` in `main.dart`
- [ ] `ProviderScope` wrapping the app
- [ ] Fonts from `google_fonts` package
- [ ] All screens follow feature-based folder structure
- [ ] `Form` + `TextFormField` with `validator` on all auth screens
- [ ] `SafeArea` on all screens
- [ ] Loading states with `CircularProgressIndicator`
- [ ] `GoRouter` navigation (no `Navigator.push`)
- [ ] `dispose()` controllers to avoid memory leaks
