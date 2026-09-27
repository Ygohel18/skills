# Stack: Android — Classic XML (View System)

## Overview
The traditional Android UI system using XML layouts + Java/Kotlin View binding. Best for targeting older API levels, maintaining legacy codebases, or teams more comfortable with XML-based design.

---

## Project Setup

Android Studio → New Project → **Empty Views Activity**.

### build.gradle.kts (app-level)
```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace  = "com.example.app"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.app"
        minSdk        = 21
        targetSdk     = 35
        versionCode   = 1
        versionName   = "1.0"
    }

    buildFeatures {
        viewBinding = true   // enables ViewBinding
    }
}

dependencies {
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.constraintlayout:constraintlayout:2.2.0")
    implementation("androidx.navigation:navigation-fragment-ktx:2.8.5")
    implementation("androidx.navigation:navigation-ui-ktx:2.8.5")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.7")
    implementation("androidx.lifecycle:lifecycle-livedata-ktx:2.8.7")
    implementation("com.github.bumptech.glide:glide:4.16.0")
    implementation("androidx.recyclerview:recyclerview:1.3.2")
    implementation("androidx.swiperefreshlayout:swiperefreshlayout:1.1.0")
}
```

---

## Theme Setup (res/values/themes.xml)

```xml
<!-- res/values/themes.xml -->
<resources xmlns:tools="http://schemas.android.com/tools">
  <style name="Theme.App" parent="Theme.MaterialComponents.DayNight.NoActionBar">
    <!-- Primary brand color from DESIGN.md -->
    <item name="colorPrimary">@color/primary</item>
    <item name="colorPrimaryVariant">@color/primary_dark</item>
    <item name="colorOnPrimary">@color/on_primary</item>
    <item name="colorSecondary">@color/secondary</item>
    <item name="colorSurface">@color/surface</item>
    <item name="colorOnSurface">@color/on_surface</item>
    <item name="android:colorBackground">@color/background</item>
    <item name="colorError">@color/error</item>

    <!-- Shape -->
    <item name="shapeAppearanceSmallComponent">@style/ShapeSmall</item>
    <item name="shapeAppearanceMediumComponent">@style/ShapeMedium</item>
    <item name="shapeAppearanceLargeComponent">@style/ShapeLarge</item>

    <!-- Typography -->
    <item name="textAppearanceHeadline1">@style/TextAppearance.App.H1</item>
    <item name="textAppearanceHeadline2">@style/TextAppearance.App.H2</item>
    <item name="textAppearanceBody1">@style/TextAppearance.App.Body1</item>
    <item name="textAppearanceBody2">@style/TextAppearance.App.Body2</item>
  </style>

  <!-- Shape system -->
  <style name="ShapeSmall"  parent="ShapeAppearance.Material3.SmallComponent">
    <item name="cornerSize">8dp</item>
  </style>
  <style name="ShapeMedium" parent="ShapeAppearance.Material3.MediumComponent">
    <item name="cornerSize">12dp</item>
  </style>
  <style name="ShapeLarge"  parent="ShapeAppearance.Material3.LargeComponent">
    <item name="cornerSize">20dp</item>
  </style>
</resources>
```

### res/values/colors.xml
```xml
<resources>
  <!-- Map DESIGN.md color tokens to Android color resources -->
  <color name="primary">#YOUR_PRIMARY</color>
  <color name="primary_dark">#YOUR_PRIMARY_DARK</color>
  <color name="on_primary">#FFFFFF</color>
  <color name="secondary">#YOUR_SECONDARY</color>
  <color name="background">#YOUR_BG</color>
  <color name="surface">#YOUR_SURFACE</color>
  <color name="on_surface">#YOUR_TEXT</color>
  <color name="on_background">#YOUR_TEXT</color>
  <color name="text_muted">#YOUR_MUTED</color>
  <color name="border">#YOUR_BORDER</color>
  <color name="error">#EF4444</color>
</resources>
```

### res/values/typography.xml
```xml
<resources>
  <!-- Download font and add to res/font/ -->
  <style name="TextAppearance.App.H1" parent="TextAppearance.Material3.DisplayMedium">
    <item name="fontFamily">@font/inter_bold</item>
    <item name="android:textSize">32sp</item>
    <item name="android:textStyle">bold</item>
  </style>
  <style name="TextAppearance.App.H2" parent="TextAppearance.Material3.HeadlineMedium">
    <item name="fontFamily">@font/inter_semibold</item>
    <item name="android:textSize">24sp</item>
  </style>
  <style name="TextAppearance.App.Body1" parent="TextAppearance.Material3.BodyLarge">
    <item name="fontFamily">@font/inter_regular</item>
    <item name="android:textSize">16sp</item>
  </style>
  <style name="TextAppearance.App.Body2" parent="TextAppearance.Material3.BodyMedium">
    <item name="fontFamily">@font/inter_regular</item>
    <item name="android:textSize">14sp</item>
  </style>
</resources>
```

---

## Navigation Graph (res/navigation/nav_graph.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/nav_graph"
    app:startDestination="@id/homeFragment">

  <fragment android:id="@+id/homeFragment"    android:name="com.example.app.ui.HomeFragment" />
  <fragment android:id="@+id/aboutFragment"   android:name="com.example.app.ui.AboutFragment" />
  <fragment android:id="@+id/blogFragment"    android:name="com.example.app.ui.BlogFragment" />
  <fragment android:id="@+id/blogDetailFragment" android:name="com.example.app.ui.BlogDetailFragment">
    <argument android:name="slug" app:argType="string" />
  </fragment>
  <fragment android:id="@+id/loginFragment"   android:name="com.example.app.ui.auth.LoginFragment" />
  <fragment android:id="@+id/registerFragment" android:name="com.example.app.ui.auth.RegisterFragment" />
  <fragment android:id="@+id/forgotPasswordFragment" android:name="com.example.app.ui.auth.ForgotPasswordFragment" />
  <fragment android:id="@+id/otpFragment"     android:name="com.example.app.ui.auth.OtpFragment" />
  <fragment android:id="@+id/profileFragment" android:name="com.example.app.ui.ProfileFragment" />
</navigation>
```

---

## File Structure

```
app/src/main/
├── java/com/example/app/
│   ├── MainActivity.kt
│   ├── ui/
│   │   ├── HomeFragment.kt
│   │   ├── AboutFragment.kt
│   │   ├── BlogFragment.kt
│   │   ├── BlogDetailFragment.kt
│   │   ├── ProfileFragment.kt
│   │   └── auth/
│   │       ├── LoginFragment.kt
│   │       ├── RegisterFragment.kt
│   │       ├── ForgotPasswordFragment.kt
│   │       └── OtpFragment.kt
│   ├── adapter/
│   │   └── BlogAdapter.kt
│   └── viewmodel/
│       └── AuthViewModel.kt
└── res/
    ├── layout/
    │   ├── activity_main.xml
    │   ├── fragment_home.xml
    │   ├── fragment_login.xml
    │   ├── fragment_register.xml
    │   ├── fragment_blog.xml
    │   ├── fragment_blog_detail.xml
    │   └── item_blog_card.xml
    ├── navigation/
    │   └── nav_graph.xml
    ├── values/
    │   ├── themes.xml
    │   ├── colors.xml
    │   └── typography.xml
    ├── drawable/
    └── font/
        ├── inter_regular.ttf
        ├── inter_medium.ttf
        ├── inter_semibold.ttf
        └── inter_bold.ttf
```

---

## Key XML Layout Patterns

### Login Fragment Layout (res/layout/fragment_login.xml)
```xml
<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/background"
    android:fillViewport="true">

  <LinearLayout
      android:layout_width="match_parent"
      android:layout_height="wrap_content"
      android:orientation="vertical"
      android:padding="24dp"
      android:gravity="center_horizontal">

    <TextView
        android:id="@+id/tv_brand"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="48dp"
        android:text="BrandName"
        android:textColor="@color/primary"
        android:textSize="28sp"
        android:textStyle="bold"
        android:fontFamily="@font/inter_bold" />

    <TextView
        android:id="@+id/tv_title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="12dp"
        android:text="Sign in to your account"
        android:textSize="22sp"
        android:textStyle="bold"
        android:fontFamily="@font/inter_semibold"
        android:textColor="@color/on_surface" />

    <!-- Card container -->
    <com.google.android.material.card.MaterialCardView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="32dp"
        app:cardCornerRadius="20dp"
        app:cardElevation="4dp"
        app:cardBackgroundColor="@color/surface">

      <LinearLayout
          android:layout_width="match_parent"
          android:layout_height="wrap_content"
          android:orientation="vertical"
          android:padding="24dp">

        <com.google.android.material.textfield.TextInputLayout
            android:id="@+id/til_email"
            style="@style/Widget.MaterialComponents.TextInputLayout.OutlinedBox"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Email"
            app:boxCornerRadiusTopStart="12dp"
            app:boxCornerRadiusTopEnd="12dp"
            app:boxCornerRadiusBottomStart="12dp"
            app:boxCornerRadiusBottomEnd="12dp">

          <com.google.android.material.textfield.TextInputEditText
              android:id="@+id/et_email"
              android:layout_width="match_parent"
              android:layout_height="wrap_content"
              android:inputType="textEmailAddress" />
        </com.google.android.material.textfield.TextInputLayout>

        <com.google.android.material.textfield.TextInputLayout
            android:id="@+id/til_password"
            style="@style/Widget.MaterialComponents.TextInputLayout.OutlinedBox"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="12dp"
            android:hint="Password"
            app:endIconMode="password_toggle"
            app:boxCornerRadiusTopStart="12dp"
            app:boxCornerRadiusTopEnd="12dp"
            app:boxCornerRadiusBottomStart="12dp"
            app:boxCornerRadiusBottomEnd="12dp">

          <com.google.android.material.textfield.TextInputEditText
              android:id="@+id/et_password"
              android:layout_width="match_parent"
              android:layout_height="wrap_content"
              android:inputType="textPassword" />
        </com.google.android.material.textfield.TextInputLayout>

        <com.google.android.material.button.MaterialButton
            android:id="@+id/btn_login"
            android:layout_width="match_parent"
            android:layout_height="52dp"
            android:layout_marginTop="20dp"
            android:text="Sign In"
            app:cornerRadius="12dp" />

      </LinearLayout>
    </com.google.android.material.card.MaterialCardView>

    <TextView
        android:id="@+id/tv_register_link"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="24dp"
        android:text="Don't have an account? Sign up"
        android:textColor="@color/text_muted"
        android:textSize="14sp" />

  </LinearLayout>
</ScrollView>
```

### Login Fragment Kotlin
```kotlin
class LoginFragment : Fragment(R.layout.fragment_login) {

    private var _binding: FragmentLoginBinding? = null
    private val binding get() = _binding!!
    private val viewModel: AuthViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentLoginBinding.bind(view)

        binding.btnLogin.setOnClickListener {
            val email    = binding.etEmail.text.toString().trim()
            val password = binding.etPassword.text.toString().trim()

            if (!android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
                binding.tilEmail.error = "Enter a valid email"
                return@setOnClickListener
            }
            if (password.length < 6) {
                binding.tilPassword.error = "Password too short"
                return@setOnClickListener
            }
            binding.tilEmail.error    = null
            binding.tilPassword.error = null
            viewModel.login(email, password)
        }

        binding.tvRegisterLink.setOnClickListener {
            findNavController().navigate(R.id.registerFragment)
        }

        viewModel.loginState.observe(viewLifecycleOwner) { state ->
            when (state) {
                is AuthState.Loading -> binding.btnLogin.isEnabled = false
                is AuthState.Success -> findNavController().navigate(R.id.homeFragment)
                is AuthState.Error   -> {
                    binding.btnLogin.isEnabled = true
                    Snackbar.make(view, state.message, Snackbar.LENGTH_SHORT).show()
                }
                else -> binding.btnLogin.isEnabled = true
            }
        }
    }

    override fun onDestroyView() { super.onDestroyView(); _binding = null }
}
```

---

## RecyclerView + ViewBinding Pattern (Blog List)

```kotlin
class BlogAdapter(
    private val items: List<BlogPost>,
    private val onItemClick: (BlogPost) -> Unit,
) : RecyclerView.Adapter<BlogAdapter.VH>() {

    inner class VH(val binding: ItemBlogCardBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) = VH(
        ItemBlogCardBinding.inflate(LayoutInflater.from(parent.context), parent, false)
    )

    override fun onBindViewHolder(holder: VH, position: Int) {
        val post = items[position]
        holder.binding.tvTitle.text   = post.title
        holder.binding.tvExcerpt.text = post.excerpt
        holder.binding.tvDate.text    = post.date
        Glide.with(holder.binding.ivThumb).load(post.imageUrl).into(holder.binding.ivThumb)
        holder.binding.root.setOnClickListener { onItemClick(post) }
    }

    override fun getItemCount() = items.size
}
```

---

## Checklist

- [ ] `viewBinding = true` in build.gradle.kts
- [ ] Material Components dependency added
- [ ] `themes.xml` with colorPrimary from DESIGN.md
- [ ] `colors.xml` with all DESIGN.md color tokens
- [ ] Font files in `res/font/` + font family XMLs
- [ ] `nav_graph.xml` with all fragments
- [ ] `MaterialCardView` for card layouts
- [ ] `TextInputLayout` (outlined) for all inputs
- [ ] `MaterialButton` for all buttons
- [ ] ViewBinding used in all Fragments (no `findViewById`)
- [ ] ViewModel + LiveData for all state
- [ ] `_binding = null` in `onDestroyView()`
- [ ] RecyclerView + Adapter for all list screens
