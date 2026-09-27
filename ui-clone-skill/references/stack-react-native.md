# Stack: React Native (Cross-Platform Mobile)

## Overview
Facebook's cross-platform mobile framework. Write JavaScript/TypeScript components that compile to native iOS and Android views. Uses React Navigation for routing and NativeWind (Tailwind) or StyleSheet for styling.

---

## Project Setup

```bash
npx react-native@latest init ProjectName --template react-native-template-typescript
cd ProjectName

# Core dependencies
npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context
npm install react-native-gesture-handler react-native-reanimated
npm install react-native-vector-icons @react-native-async-storage/async-storage

# NativeWind (Tailwind for React Native)
npm install nativewind tailwindcss
npx tailwindcss init
```

### tailwind.config.js (NativeWind)
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./App.{js,jsx,ts,tsx}', './src/**/*.{js,jsx,ts,tsx}'],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        primary:    '#YOUR_PRIMARY',
        secondary:  '#YOUR_SECONDARY',
        surface:    '#YOUR_SURFACE',
        background: '#YOUR_BG',
        muted:      '#YOUR_MUTED',
        border:     '#YOUR_BORDER',
      },
      fontFamily: {
        sans:    ['Inter-Regular'],
        heading: ['Inter-Bold'],
      },
    },
  },
  plugins: [],
};
```

### babel.config.js
```js
module.exports = {
  presets: ['module:@react-native/babel-preset'],
  plugins: [
    'nativewind/babel',
    'react-native-reanimated/plugin',   // must be last
  ],
};
```

---

## Theme (Design Tokens)

### src/theme/colors.ts
```ts
// Map all DESIGN.md color tokens to JS constants
export const Colors = {
  primary:        '#YOUR_PRIMARY',
  primaryLight:   '#YOUR_PRIMARY_LIGHT',
  secondary:      '#YOUR_SECONDARY',
  background:     '#YOUR_BG',
  surface:        '#YOUR_SURFACE',
  onPrimary:      '#FFFFFF',
  text:           '#YOUR_TEXT',
  textMuted:      '#YOUR_MUTED',
  border:         '#YOUR_BORDER',
  error:          '#EF4444',
  success:        '#22C55E',
  warning:        '#F59E0B',
  // dark variants
  backgroundDark: '#0F172A',
  surfaceDark:    '#1E293B',
  textDark:       '#F1F5F9',
} as const;
```

### src/theme/typography.ts
```ts
import { StyleSheet } from 'react-native';

export const Typography = StyleSheet.create({
  h1:      { fontSize: 32, fontWeight: '700', fontFamily: 'Inter-Bold',     lineHeight: 40 },
  h2:      { fontSize: 24, fontWeight: '600', fontFamily: 'Inter-SemiBold', lineHeight: 32 },
  h3:      { fontSize: 20, fontWeight: '600', fontFamily: 'Inter-SemiBold', lineHeight: 28 },
  body:    { fontSize: 16, fontWeight: '400', fontFamily: 'Inter-Regular',  lineHeight: 24 },
  bodyMd:  { fontSize: 14, fontWeight: '400', fontFamily: 'Inter-Regular',  lineHeight: 20 },
  label:   { fontSize: 14, fontWeight: '600', fontFamily: 'Inter-SemiBold', lineHeight: 20 },
  caption: { fontSize: 12, fontWeight: '400', fontFamily: 'Inter-Regular',  lineHeight: 16 },
});
```

---

## Navigation Setup

### src/navigation/AppNavigator.tsx
```tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator }       from '@react-navigation/stack';
import { createBottomTabNavigator }   from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/Feather';
import { Colors } from '../theme/colors';

import HomeScreen          from '../screens/HomeScreen';
import BlogScreen          from '../screens/BlogScreen';
import BlogDetailScreen    from '../screens/BlogDetailScreen';
import ProfileScreen       from '../screens/ProfileScreen';
import LoginScreen         from '../screens/auth/LoginScreen';
import RegisterScreen      from '../screens/auth/RegisterScreen';
import ForgotPasswordScreen from '../screens/auth/ForgotPasswordScreen';
import OtpScreen           from '../screens/auth/OtpScreen';

export type RootStackParamList = {
  Main:           undefined;
  Login:          undefined;
  Register:       undefined;
  ForgotPassword: undefined;
  Otp:            undefined;
  BlogDetail:     { slug: string };
};

export type TabParamList = {
  Home:    undefined;
  Blog:    undefined;
  Profile: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();
const Tab   = createBottomTabNavigator<TabParamList>();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor:   Colors.primary,
        tabBarInactiveTintColor: Colors.textMuted,
        tabBarStyle: { borderTopColor: Colors.border, backgroundColor: Colors.surface },
        tabBarIcon: ({ focused, color, size }) => {
          const icons: Record<string, string> = { Home: 'home', Blog: 'book-open', Profile: 'user' };
          return <Icon name={icons[route.name]} size={size} color={color} />;
        },
      })}>
      <Tab.Screen name="Home"    component={HomeScreen} />
      <Tab.Screen name="Blog"    component={BlogScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Main"           component={TabNavigator} />
        <Stack.Screen name="Login"          component={LoginScreen} />
        <Stack.Screen name="Register"       component={RegisterScreen} />
        <Stack.Screen name="ForgotPassword" component={ForgotPasswordScreen} />
        <Stack.Screen name="Otp"            component={OtpScreen} />
        <Stack.Screen name="BlogDetail"     component={BlogDetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

---

## File Structure

```
src/
├── components/
│   ├── AppButton.tsx
│   ├── AppCard.tsx
│   ├── AppInput.tsx
│   ├── AppHeader.tsx
│   └── Badge.tsx
├── screens/
│   ├── HomeScreen.tsx
│   ├── BlogScreen.tsx
│   ├── BlogDetailScreen.tsx
│   ├── ProfileScreen.tsx
│   └── auth/
│       ├── LoginScreen.tsx
│       ├── RegisterScreen.tsx
│       ├── ForgotPasswordScreen.tsx
│       └── OtpScreen.tsx
├── navigation/
│   └── AppNavigator.tsx
├── theme/
│   ├── colors.ts
│   └── typography.ts
├── hooks/
│   └── useAuth.ts
└── store/
    └── authStore.ts
```

---

## Key Component Patterns

### AppButton
```tsx
// src/components/AppButton.tsx
import React from 'react';
import { TouchableOpacity, Text, ActivityIndicator, StyleSheet, ViewStyle } from 'react-native';
import { Colors } from '../theme/colors';

type Variant = 'primary' | 'outline' | 'ghost';

interface AppButtonProps {
  title:      string;
  onPress:    () => void;
  variant?:   Variant;
  isLoading?: boolean;
  disabled?:  boolean;
  style?:     ViewStyle;
}

export function AppButton({ title, onPress, variant = 'primary', isLoading, disabled, style }: AppButtonProps) {
  const styles = getStyles(variant);
  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={isLoading || disabled}
      activeOpacity={0.8}
      style={[styles.button, (isLoading || disabled) && styles.disabled, style]}>
      {isLoading
        ? <ActivityIndicator color={variant === 'primary' ? '#fff' : Colors.primary} size="small" />
        : <Text style={styles.label}>{title}</Text>}
    </TouchableOpacity>
  );
}

const getStyles = (variant: Variant) => StyleSheet.create({
  button: {
    height: 52, borderRadius: 12, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 24,
    ...(variant === 'primary'  && { backgroundColor: Colors.primary }),
    ...(variant === 'outline'  && { borderWidth: 1.5, borderColor: Colors.primary, backgroundColor: 'transparent' }),
    ...(variant === 'ghost'    && { backgroundColor: 'transparent' }),
  },
  label: {
    fontSize: 16, fontWeight: '600', fontFamily: 'Inter-SemiBold',
    color: variant === 'primary' ? '#fff' : Colors.primary,
  },
  disabled: { opacity: 0.5 },
});
```

### LoginScreen
```tsx
// src/screens/auth/LoginScreen.tsx
import React, { useState } from 'react';
import {
  View, Text, TextInput, KeyboardAvoidingView,
  Platform, ScrollView, StyleSheet, TouchableOpacity,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { AppButton } from '../../components/AppButton';
import { Colors } from '../../theme/colors';
import { Typography } from '../../theme/typography';

export default function LoginScreen() {
  const navigation = useNavigation();
  const [email,     setEmail]     = useState('');
  const [password,  setPassword]  = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errors,    setErrors]    = useState<{ email?: string; password?: string }>({});

  const validate = () => {
    const e: typeof errors = {};
    if (!email.includes('@'))     e.email    = 'Enter a valid email';
    if (password.length < 6)      e.password = 'Minimum 6 characters';
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleLogin = async () => {
    if (!validate()) return;
    setIsLoading(true);
    // TODO: call auth API
    await new Promise(r => setTimeout(r, 1000));
    setIsLoading(false);
    navigation.navigate('Main' as never);
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
        <Text style={styles.brand}>BrandName</Text>
        <Text style={[Typography.h2, styles.title]}>Sign in to your account</Text>
        <Text style={[Typography.body, styles.subtitle]}>Welcome back!</Text>

        <View style={styles.card}>
          <View style={styles.fieldGroup}>
            <Text style={styles.label}>Email</Text>
            <TextInput
              style={[styles.input, errors.email && styles.inputError]}
              placeholder="you@example.com"
              keyboardType="email-address"
              autoCapitalize="none"
              value={email}
              onChangeText={setEmail}
            />
            {errors.email && <Text style={styles.errorText}>{errors.email}</Text>}
          </View>

          <View style={styles.fieldGroup}>
            <Text style={styles.label}>Password</Text>
            <TextInput
              style={[styles.input, errors.password && styles.inputError]}
              placeholder="••••••••"
              secureTextEntry
              value={password}
              onChangeText={setPassword}
            />
            {errors.password && <Text style={styles.errorText}>{errors.password}</Text>}
          </View>

          <TouchableOpacity onPress={() => navigation.navigate('ForgotPassword' as never)}
                            style={styles.forgotLink}>
            <Text style={styles.forgotText}>Forgot password?</Text>
          </TouchableOpacity>

          <AppButton title="Sign In" onPress={handleLogin} isLoading={isLoading} style={styles.loginBtn} />
        </View>

        <View style={styles.registerRow}>
          <Text style={[Typography.bodyMd, { color: Colors.textMuted }]}>Don't have an account? </Text>
          <TouchableOpacity onPress={() => navigation.navigate('Register' as never)}>
            <Text style={[Typography.bodyMd, { color: Colors.primary, fontWeight: '600' }]}>Sign up</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container:   { flex: 1, backgroundColor: Colors.background },
  scroll:      { flexGrow: 1, padding: 24, alignItems: 'center' },
  brand:       { fontSize: 28, fontWeight: '700', color: Colors.primary, marginTop: 48 },
  title:       { textAlign: 'center', marginTop: 8 },
  subtitle:    { color: Colors.textMuted, marginTop: 4 },
  card:        { width: '100%', backgroundColor: Colors.surface, borderRadius: 20, padding: 24, marginTop: 32,
                 shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.08, shadowRadius: 12, elevation: 4 },
  fieldGroup:  { marginBottom: 16 },
  label:       { fontSize: 14, fontWeight: '500', color: Colors.text, marginBottom: 6 },
  input:       { borderWidth: 1.5, borderColor: Colors.border, borderRadius: 12, padding: 14, fontSize: 16, color: Colors.text },
  inputError:  { borderColor: Colors.error },
  errorText:   { color: Colors.error, fontSize: 12, marginTop: 4 },
  forgotLink:  { alignSelf: 'flex-end', marginBottom: 8 },
  forgotText:  { color: Colors.primary, fontSize: 13, fontWeight: '500' },
  loginBtn:    { marginTop: 8 },
  registerRow: { flexDirection: 'row', alignItems: 'center', marginTop: 24 },
});
```

---

## NativeWind (Tailwind) Alternative

If using NativeWind instead of StyleSheet:

```tsx
// Instead of StyleSheet, use className prop
<View className="flex-1 bg-background p-6">
  <Text className="text-3xl font-bold text-primary">BrandName</Text>
  <TouchableOpacity className="bg-primary rounded-xl py-3.5 items-center mt-4">
    <Text className="text-white font-semibold text-base">Sign In</Text>
  </TouchableOpacity>
</View>
```

---

## Checklist

- [ ] React Navigation installed + `NavigationContainer` in App.tsx
- [ ] Stack + Tab navigator configured with all screens
- [ ] `Colors.ts` with all DESIGN.md color tokens
- [ ] `Typography.ts` with all text styles
- [ ] Custom fonts registered (iOS: Info.plist, Android: assets/fonts/)
- [ ] `AppButton`, `AppInput`, `AppCard` reusable components
- [ ] `KeyboardAvoidingView` on all auth screens
- [ ] Platform-specific `behavior` for KeyboardAvoidingView
- [ ] Form validation before API calls
- [ ] Loading states with `ActivityIndicator`
- [ ] `SafeAreaView` or `useSafeAreaInsets()` for notch/home bar
- [ ] All screens properly typed with `StackParamList`
