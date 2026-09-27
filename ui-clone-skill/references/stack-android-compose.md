# Stack: Android — Jetpack Compose (Modern Declarative UI)

## Overview
Kotlin-first, fully declarative UI framework for Android. Best for new Android apps targeting API 21+ with Material 3 design system.

---

## Project Setup

Create via Android Studio → New Project → **Empty Activity** (Compose).

### build.gradle.kts (app-level)
```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}

android {
    namespace     = "com.example.app"
    compileSdk    = 35

    defaultConfig {
        applicationId  = "com.example.app"
        minSdk         = 24
        targetSdk      = 35
        versionCode    = 1
        versionName    = "1.0"
    }

    buildFeatures { compose = true }
}

dependencies {
    // Compose BOM — manages all Compose library versions
    val composeBom = platform("androidx.compose:compose-bom:2024.12.01")
    implementation(composeBom)

    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.activity:activity-compose:1.10.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
    implementation("androidx.navigation:navigation-compose:2.8.5")
    implementation("io.coil-kt.coil3:coil-compose:3.0.4")

    debugImplementation("androidx.compose.ui:ui-tooling")
}
```

---

## Theme Setup (from DESIGN.md)

### ui/theme/Color.kt
```kotlin
package com.example.app.ui.theme

import androidx.compose.ui.graphics.Color

// Map all DESIGN.md colors to Compose Color objects
val Primary       = Color(0xFF_YOUR_PRIMARY)    // e.g. Color(0xFF6366F1)
val PrimaryContainer = Color(0xFF_YOUR_PRIMARY_CONTAINER)
val Secondary     = Color(0xFF_YOUR_SECONDARY)
val Background    = Color(0xFF_YOUR_BG)
val Surface       = Color(0xFF_YOUR_SURFACE)
val OnPrimary     = Color(0xFFFFFFFF)
val OnBackground  = Color(0xFF_YOUR_TEXT)
val OnSurface     = Color(0xFF_YOUR_TEXT)
val Error         = Color(0xFFEF4444)

// Dark mode variants
val PrimaryDark   = Color(0xFF_YOUR_PRIMARY_DARK)
val BackgroundDark = Color(0xFF0F172A)
val SurfaceDark   = Color(0xFF1E293B)
```

### ui/theme/Type.kt
```kotlin
package com.example.app.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.example.app.R

// Add your font file to res/font/ folder
val InterFamily = FontFamily(
    Font(R.font.inter_regular,   FontWeight.Normal),
    Font(R.font.inter_medium,    FontWeight.Medium),
    Font(R.font.inter_semibold,  FontWeight.SemiBold),
    Font(R.font.inter_bold,      FontWeight.Bold),
)

val AppTypography = Typography(
    displayLarge  = TextStyle(fontFamily = InterFamily, fontWeight = FontWeight.Bold,   fontSize = 57.sp, lineHeight = 64.sp),
    headlineLarge = TextStyle(fontFamily = InterFamily, fontWeight = FontWeight.Bold,   fontSize = 32.sp, lineHeight = 40.sp),
    headlineMedium = TextStyle(fontFamily = InterFamily, fontWeight = FontWeight.SemiBold, fontSize = 24.sp, lineHeight = 32.sp),
    titleLarge    = TextStyle(fontFamily = InterFamily, fontWeight = FontWeight.SemiBold, fontSize = 20.sp, lineHeight = 28.sp),
    bodyLarge     = TextStyle(fontFamily = InterFamily, fontWeight = FontWeight.Normal, fontSize = 16.sp, lineHeight = 24.sp),
    bodyMedium    = TextStyle(fontFamily = InterFamily, fontWeight = FontWeight.Normal, fontSize = 14.sp, lineHeight = 20.sp),
    labelLarge    = TextStyle(fontFamily = InterFamily, fontWeight = FontWeight.Medium, fontSize = 14.sp, lineHeight = 20.sp),
    labelSmall    = TextStyle(fontFamily = InterFamily, fontWeight = FontWeight.Medium, fontSize = 11.sp, lineHeight = 16.sp),
)
```

### ui/theme/Theme.kt
```kotlin
package com.example.app.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

private val LightColorScheme = lightColorScheme(
    primary          = Primary,
    onPrimary        = OnPrimary,
    primaryContainer = PrimaryContainer,
    secondary        = Secondary,
    background       = Background,
    surface          = Surface,
    onBackground     = OnBackground,
    onSurface        = OnSurface,
    error            = Error,
)

private val DarkColorScheme = darkColorScheme(
    primary          = PrimaryDark,
    onPrimary        = OnPrimary,
    background       = BackgroundDark,
    surface          = SurfaceDark,
)

@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false,       // set true to use Material You wallpaper colors
    content: @Composable () -> Unit,
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val ctx = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(ctx) else dynamicLightColorScheme(ctx)
        }
        darkTheme -> DarkColorScheme
        else      -> LightColorScheme
    }
    MaterialTheme(colorScheme = colorScheme, typography = AppTypography, content = content)
}
```

---

## Navigation Setup

```kotlin
// navigation/AppNavGraph.kt
package com.example.app.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.example.app.ui.screens.*

sealed class Screen(val route: String) {
    object Home      : Screen("home")
    object About     : Screen("about")
    object Blog      : Screen("blog")
    object BlogDetail: Screen("blog/{slug}") {
        fun createRoute(slug: String) = "blog/$slug"
    }
    object Login     : Screen("login")
    object Register  : Screen("register")
    object ForgotPassword : Screen("forgot-password")
    object Otp       : Screen("otp")
    object Profile   : Screen("profile")
}

@Composable
fun AppNavGraph(navController: NavHostController) {
    NavHost(navController = navController, startDestination = Screen.Home.route) {
        composable(Screen.Home.route)       { HomeScreen(navController) }
        composable(Screen.About.route)      { AboutScreen(navController) }
        composable(Screen.Blog.route)       { BlogScreen(navController) }
        composable(Screen.BlogDetail.route) { backStack ->
            BlogDetailScreen(navController, slug = backStack.arguments?.getString("slug") ?: "")
        }
        composable(Screen.Login.route)      { LoginScreen(navController) }
        composable(Screen.Register.route)   { RegisterScreen(navController) }
        composable(Screen.ForgotPassword.route) { ForgotPasswordScreen(navController) }
        composable(Screen.Otp.route)        { OtpScreen(navController) }
        composable(Screen.Profile.route)    { ProfileScreen(navController) }
    }
}
```

---

## Screen Structure

```
app/src/main/java/com/example/app/
├── MainActivity.kt
├── navigation/
│   └── AppNavGraph.kt
├── ui/
│   ├── theme/
│   │   ├── Color.kt
│   │   ├── Type.kt
│   │   └── Theme.kt
│   ├── components/
│   │   ├── AppButton.kt
│   │   ├── AppCard.kt
│   │   ├── AppTextField.kt
│   │   ├── AppTopBar.kt
│   │   └── BottomNavBar.kt
│   └── screens/
│       ├── HomeScreen.kt
│       ├── AboutScreen.kt
│       ├── BlogScreen.kt
│       ├── BlogDetailScreen.kt
│       ├── LoginScreen.kt
│       ├── RegisterScreen.kt
│       ├── ForgotPasswordScreen.kt
│       ├── OtpScreen.kt
│       └── ProfileScreen.kt
└── viewmodel/
    └── AuthViewModel.kt
```

---

## Key Compose Component Patterns

### AppButton
```kotlin
@Composable
fun AppButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    variant: ButtonVariant = ButtonVariant.Primary,
    isLoading: Boolean = false,
) {
    when (variant) {
        ButtonVariant.Primary -> Button(
            onClick = onClick, modifier = modifier.fillMaxWidth().height(52.dp),
            shape = RoundedCornerShape(12.dp),
            enabled = !isLoading,
        ) {
            if (isLoading) {
                CircularProgressIndicator(modifier = Modifier.size(20.dp),
                    color = MaterialTheme.colorScheme.onPrimary, strokeWidth = 2.dp)
            } else {
                Text(text, style = MaterialTheme.typography.labelLarge)
            }
        }
        ButtonVariant.Outline -> OutlinedButton(
            onClick = onClick, modifier = modifier.fillMaxWidth().height(52.dp),
            shape = RoundedCornerShape(12.dp),
        ) {
            Text(text, style = MaterialTheme.typography.labelLarge)
        }
        ButtonVariant.Ghost -> TextButton(
            onClick = onClick, modifier = modifier,
        ) {
            Text(text, style = MaterialTheme.typography.labelLarge)
        }
    }
}

enum class ButtonVariant { Primary, Outline, Ghost }
```

### LoginScreen
```kotlin
@Composable
fun LoginScreen(navController: NavController) {
    val viewModel: AuthViewModel = viewModel()

    Column(
        modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)
            .padding(24.dp).verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Spacer(Modifier.height(48.dp))

        // Logo / Brand
        Text("BrandName", style = MaterialTheme.typography.headlineLarge,
             color = MaterialTheme.colorScheme.primary)

        Spacer(Modifier.height(8.dp))
        Text("Sign in to your account", style = MaterialTheme.typography.titleLarge,
             color = MaterialTheme.colorScheme.onBackground)
        Text("Welcome back!", style = MaterialTheme.typography.bodyMedium,
             color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f))

        Spacer(Modifier.height(40.dp))

        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        ) {
            Column(modifier = Modifier.padding(24.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedTextField(
                    value = viewModel.email,
                    onValueChange = { viewModel.email = it },
                    label = { Text("Email") },
                    placeholder = { Text("you@example.com") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                )
                OutlinedTextField(
                    value = viewModel.password,
                    onValueChange = { viewModel.password = it },
                    label = { Text("Password") },
                    visualTransformation = PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                )
                TextButton(
                    onClick = { navController.navigate(Screen.ForgotPassword.route) },
                    modifier = Modifier.align(Alignment.End),
                ) { Text("Forgot password?", style = MaterialTheme.typography.bodySmall) }

                AppButton(text = "Sign In", onClick = { viewModel.login() }, isLoading = viewModel.isLoading)
            }
        }

        Spacer(Modifier.height(24.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Don't have an account? ", style = MaterialTheme.typography.bodyMedium)
            TextButton(onClick = { navController.navigate(Screen.Register.route) }) {
                Text("Sign up", style = MaterialTheme.typography.bodyMedium,
                     color = MaterialTheme.colorScheme.primary)
            }
        }
    }
}
```

---

## Checklist

- [ ] Compose BOM added in build.gradle.kts
- [ ] `navigation-compose` dependency added
- [ ] Theme: Color.kt, Type.kt, Theme.kt created with DESIGN.md tokens
- [ ] Custom font files in `res/font/`
- [ ] `AppNavGraph.kt` with all routes
- [ ] Material3 `AppTopBar` with back navigation
- [ ] `BottomNavBar` with primary nav items
- [ ] All screens implement `@Preview` annotations
- [ ] `viewModel()` pattern with StateFlow for all data
- [ ] Loading states with `CircularProgressIndicator`
- [ ] Error states with Snackbar or AlertDialog
