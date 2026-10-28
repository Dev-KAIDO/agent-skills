---
name: mobile-development
description: Complete mobile development skill — Expo/React Native, EAS builds and updates, Expo Router navigation, native modules, App Clips, brownfield integration, performance optimization, offline support, and React Native best practices. Use for ANY mobile app development task.
---

# Mobile Development — Complete Skill

## Overview

**Single skill for all mobile development.** Merges `building-native-ui`, `native-data-fetching`, all `expo-*` skills, `react-native-best-practices`, `upgrading-expo`, `engineering-mobile-app-builder`, `add-app-clip`, `expo-brownfield`, `expo-observe`, `eas-update-insights`, `expo-dev-client`, `expo-api-routes`, `expo-module`, and `use-dom`.

---

## 1. Expo Setup (إعداد Expo)

### 1.1 Project Creation
```bash
# Create new project
npx create-expo-app@latest my-app
cd my-app

# Start development
npx expo start              # dev server
npx expo start --ios        # iOS simulator
npx expo start --android    # Android emulator
npx expo start --web        # web browser
```

### 1.2 Expo Go vs Dev Client
| | Expo Go | Dev Client |
|---|---------|------------|
| Setup | Instant | Build required |
| Native modules | Limited (Expo SDK) | Full access |
| Custom native code | ❌ | ✅ |
| Use for | Prototyping, simple apps | Production, custom modules |

```bash
# Install dev client
npx expo install expo-dev-client
npx expo run:ios     # build + run on simulator
npx expo run:android # build + run on emulator
```

### 1.3 Expo Router (Routing)
```tsx
// app/_layout.tsx — root layout
export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="modal" options={{ presentation: 'modal' }} />
    </Stack>
  );
}

// app/(tabs)/_layout.tsx — tab layout
export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="index" options={{ title: 'Home' }} />
      <Tabs.Screen name="explore" options={{ title: 'Explore' }} />
    </Tabs>
  );
}

// app/user/[id].tsx — dynamic route
export default function UserProfile() {
  const { id } = useLocalSearchParams();
  // ...
}
```

---

## 2. Native UI (واجهة أصلية)

### 2.1 Platform-Specific Code
```tsx
// File extension approach
Component.ios.tsx    // iOS only
Component.android.tsx // Android only
Component.tsx        // shared

// Runtime approach
import { Platform } from 'react-native';
const styles = StyleSheet.create({
  container: Platform.select({
    ios: { paddingTop: 60 },      // status bar height
    android: { paddingTop: 40 },
    default: { paddingTop: 0 },   // web
  }),
});
```

### 2.2 Window Dimensions
```tsx
// ✅ Use hook (reacts to rotation)
import { useWindowDimensions } from 'react-native';
const { width, height } = useWindowDimensions();

// ❌ Don't use Dimensions.get() (static, doesn't update)
```

### 2.3 Shadows (Cross-Platform)
```tsx
// ✅ Modern (works on all platforms)
boxShadow: '0 2px 8px rgba(0,0,0,0.15)'

// ❌ Legacy (platform-specific, inconsistent)
shadowColor, shadowOffset, shadowOpacity, shadowRadius  // iOS only
elevation  // Android only
```

### 2.4 Web Code via 'use dom' (كود ويب داخل التطبيق)
Migrate web code into a React Native app incrementally:
```tsx
'use dom';   // ← directive at top of the component file

import { createIframe } from 'your-web-module';

export default function WebWidget() {
  return <div className="web-only">Runs in a webview on native, as-is on web</div>;
}
```
- **How it works:** on native, the component runs inside a webview; on web, it runs natively in the browser — one codebase, no fork
- **Use for:** complex web-only widgets (editors, charts, maps) you can't rewrite yet
- **Migration strategy:** wrap the web component, embed via `DomView`, then progressively replace with native components
- ⚠️ Don't build your WHOLE app in `use dom` — you lose native performance and platform feel
- ❌ Never use it for core navigation or primary UI; keep native for the main experience

---

## 3. Data Fetching (جلب البيانات)

### 3.1 Fetch Patterns
```tsx
// Basic fetch with error handling
async function fetchUsers() {
  try {
    const response = await fetch(`${API_URL}/users`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    return data;
  } catch (error) {
    // Handle offline, timeout, server error
    throw error;
  }
}
```

### 3.2 React Query (Recommended)
```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
    staleTime: 5 * 60 * 1000,  // 5 minutes
  });
}

function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### 3.3 Offline Support
```tsx
// Cache strategy
- React Query: persists cache automatically
- AsyncStorage: for user preferences
- SQLite: for offline-first data (with sync)

// Offline indicator
import { useNetInfo } from '@react-native-community/netinfo';
const { isConnected } = useNetInfo();
{!isConnected && <Banner message="You're offline" />}
```

### 3.4 Expo Router Data Loaders (محمّلات المسارات)
```tsx
import { useLoaderData } from 'expo-router';
import { createFileRoute } from '@tanstack/react-router'; // if using TanStack

export const Route = createFileRoute('/users/$id')({
  loader: async ({ params }) => fetchUser(params.id),
});

function UserScreen() {
  const user = useLoaderData();   // no useEffect, no loading state boilerplate
  return <Text>{user.name}</Text>;
}
```
- Loaders run before render; use `Suspense`/`pending` for the loading state
- Pair with React Query for caching; loaders for initial load, hooks for background refetch
- Reference: `references/expo-router-loaders.md`, `references/queries.md`

### 3.5 SWR Option (بديل SWR)
```tsx
import useSWR from 'swr';
const { data, error, isLoading } = useSWR('/users', fetcher);
```
- **Use React Query** for mutations + complex caching; **SWR** for simple read-heavy, hooks-first code

### 3.6 Auth & Config (المصادقة والإعداد)
```tsx
// Token management: secure storage, not AsyncStorage for sensitive tokens
import * as SecureStore from 'expo-secure-store';
const token = await SecureStore.getItemAsync('token');

// Environment-based URL config
const API_URL = process.env.EXPO_PUBLIC_API_URL;  // EXPO_PUBLIC_ prefix required
```
- ✅ Attach token via interceptor/headers; refresh on 401 with a single-flight refresh
- ✅ `EXPO_PUBLIC_*` env vars only (client bundle can't read arbitrary env)

---

## 4. Performance (الأداء)

### 4.1 List Optimization
```tsx
// ✅ FlashList (recommended over FlatList)
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={items}
  estimatedItemSize={80}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={(item) => item.id}
/>

// Memoize item component
const ItemCard = React.memo(({ item }) => (
  <View style={styles.card}>
    <Text>{item.title}</Text>
  </View>
));
```

### 4.2 Re-render Optimization
```tsx
// ✅ Memoize callbacks
const onPress = useCallback(() => {
  handlePress(id);
}, [id]);

// ✅ Memoize expensive computations
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// ✅ Stable key props
<FlatList data={items} keyExtractor={(item) => item.id} />

// ❌ Avoid inline functions in props
<FlatList renderItem={(item) => <Card item={item} />} />  // new fn each render
```

### 4.3 Bundle Size
```bash
# Analyze bundle
npx expo export --platform ios
npx react-native-bundle-visualizer

# Reduce size
- Lazy load screens (React.lazy)
- Tree shake unused code
- Compress images (expo-image)
- Remove unused dependencies
```

---

## 5. EAS Builds & Updates

### 5.1 EAS Build
```bash
# Install CLI
npm i -g eas-cli
eas login

# Configure
eas build:configure

# Development build
eas build --platform ios --profile development

# Production build
eas build --platform all --profile production

# Build status
eas build:list
```

### 5.2 EAS Update (OTA)
```bash
# Push update (bypasses app store)
eas update --branch production --message "Bug fix"

# Check update health
eas update:list
eas channel:insights production

# Rollout strategy
eas update --branch production --republish  # rollback to previous
```

### 5.3 Update Insights
| Metric | Meaning |
|--------|---------|
| **Embedded users** | On app store version |
| **OTA users** | On latest update |
| **Crash rate** | Should not increase after update |
| **Install count** | Update adoption rate |

---

## 6. Native Modules (الوحدات الأصلية)

### 6.1 Expo Module API
```typescript
// expo-module.config.json
{
  "platforms": ["ios", "android"],
  "ios": { "modules": ["MyModule"] },
}

// ios/MyModule.swift
public class MyModule: Module {
  public func definition() -> ModuleDefinition {
    Name("MyModule")

    Function("greet") { (name: String) in
      return "Hello, \(name)!"
    }

    AsyncFunction("fetchData") { (url: String, promise: Promise) in
      // async operation
    }
  }
}

// TypeScript
import MyModule from './MyModule';
const greeting = MyModule.greet('World');
```

### 6.2 When to Create Native Module
- Platform API not exposed by Expo SDK
- Performance-critical native code
- Third-party SDK integration

---

## 7. App Clip (لقطة التطبيق) — iOS Only

### 7.1 Setup
```bash
# Add App Clip target (iOS 16+)
# Xcode → File → New → Target → App Clip

# Configure AASA (Apple App Site Association)
# Place at: https://yourdomain.com/.well-known/apple-app-site-association
```

### 7.2 AASA Configuration
```json
{
  "applinks": {
    "apps": [],
    "details": [{
      "appID": "TEAMID.com.example.parentapp",
      "paths": ["/clip/*", "/store/*"]
    }]
  },
  "appclips": {
    "apps": [{
      "appID": "TEAMID.com.example.parentapp.Clip",
      "paths": ["/clip/*"]
    }]
  }
}
```

### 7.3 Rules
- App Clip < 15MB (compressed)
- Parent app must exist in App Store
- AASA must be valid and accessible
- Smart App Banner on website

---

## 8. Brownfield Integration (الدمج في تطبيق موجود)

### 8.1 Two Approaches
| Approach | Use Case |
|----------|----------|
| **Isolated** | React Native screens inside native app |
| **Integrated** | Full integration with native navigation |

### 8.2 Integration Steps
```bash
# 1. Install Expo in existing native app
npm install expo react-native

# 2. Configure app.json / app.config.js

# 3. Add Expo modules
npx expo install expo-modules-core

# 4. Embed React Native view (iOS)
# Use ExpoRootViewController

# 5. Embed React Native view (Android)
# Use ExpoReactHost
```

---

## 9. Expo API Routes (مسارات الواجهة البرمجية)

### 9.1 Server-Side API (EAS Hosting)
```tsx
// app/api/users+api.ts
export async function GET(request: Request) {
  const users = await db.users.findMany();
  return Response.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await db.users.create({ data: body });
  return Response.json(user, { status: 201 });
}
```

### 9.2 When to Use
- Simple CRUD (no complex backend)
- Webhooks
- Authentication callbacks
- Server-side rendering needs

---

## 10. Upgrading Expo (ترقية Expo)

### 10.1 Upgrade Process
```bash
# 1. Check current version
npx expo --version

# 2. Install upgrade tool
npm install -g expo-cli

# 3. Upgrade
npx expo upgrade

# 4. Fix breaking changes (run doctor)
npx expo-doctor

# 5. Test thoroughly
- iOS simulator
- Android emulator
- Production build
```

### 10.2 Common Breaking Changes
| Version Jump | Breaking Changes |
|--------------|------------------|
| SDK 50 → 51 | React Native 0.73, new blur API |
| SDK 51 → 52 | React Native 0.74, new architecture default |
| SDK 52 → 53 | React Native 0.75, API changes |

### 10.3 Major Migration Concerns (م Concerns الترحيل الكبير)
| Concern | What to do |
|---------|-----------|
| **React 19** | New hook/use API; check peer deps; test refs + `useEffect` cleanup (`references/react-19.md`) |
| **New Architecture** | TurboModules + Fabric; enable per-library; audit native deps for compatibility (`references/new-architecture.md`) |
| **React Compiler** | Memoization is automatic — remove manual `useMemo`/`useCallback` added only for perf (`references/react-compiler.md`) |
| **expo-av → expo-audio / expo-video** | `expo-av` is deprecated; migrate per the guides (`references/expo-av-to-audio.md`, `expo-av-to-video.md`) |
| **react-navigation → expo-router** | File-based routing codemod; move screens into `app/` (`references/react-navigation-to-expo-router.md`) |
| **Beta / `@next` flow** | Try a future SDK early: `npx expo install --next`, revert if blocked |

```bash
# Codemods (run, review diff, commit separately)
npx expo-codemod navigation-expo-router
npx react-native-rename ...   # only if renaming
# After upgrade:
npx expo-doctor               # dependency health
npx expo install --check      # align native dep versions
```
- ✅ Upgrade in a dedicated branch; one SDK at a time; full test after each

---

## 11. Expo Observe (قياس الأداء)

### 11.1 Metrics
| Metric | What It Measures |
|--------|-----------------|
| **Cold launch** | App start from scratch |
| **Warm launch** | App resume from background |
| **TTR** | Time to ready (interactive) |
| **TTI** | Time to interactive |
| **Route TTR** | Navigation readiness |
| **Update TTI** | OTA update install time |

### 11.2 Setup
```tsx
// App root
import { AppMetricsRoot } from 'expo-observe';

export default function App() {
  return (
    <AppMetricsRoot>
      <RootNavigator />
    </AppMetricsRoot>
  );
}

// Route-level metrics
import { useObserveRoute } from 'expo-observe';
useObserveRoute();
```

### 11.3 CLI Query Commands (أوامر الاستعلام)
```bash
eas observe:metrics-summary   # cold/warm launch, TTR, TTI rollup
eas observe:routes            # per-navigation cold/warm TTR
eas observe:events            # raw event stream
eas observe:versions          # metrics per update version (embedded vs OTA)
eas observe:metrics           # detailed metrics query
```
- **TTI frameRate params** in metrics help diagnose jank during startup
- Use `observe:versions` to compare embedded-build users vs OTA-update users
- Requires `expo-observe` + `eas observe` access

---

## Bundled References (المراجع المرفقة)
72 reference docs in `references/` — consult before deep work:

| Topic | Files |
|-------|-------|
| Native UI | `native-tabs.md`, `controls.md`, `form-sheet.md`, `gradients.md`, `icons.md`, `media.md`, `search.md`, `storage.md`, `tabs.md`, `toolbar-and-headers.md`, `visual-effects.md`, `zoom-transitions.md`, `route-structure.md`, `animations.md`, `js-animations-reanimated.md` |
| Performance | `bundle-*.md` (hermes, tree-shaking, code-splitting, r8, barrel-exports, …), `native-*.md` (measure-tti, memory-leaks, profiling, turbo-modules), `js-*.md` (measure-fps, memory-leaks, profile-react, concurrent-react) |
| React 19 & Compiler | `react-19.md`, `react-compiler.md`, `js-react-compiler.md`, `js-atomic-state.md`, `js-uncontrolled-components.md` |
| Architecture | `new-architecture.md`, `native-threading-model.md`, `native-view-flattening.md`, `native-sdks-over-polyfills.md` |
| Upgrades | `expo-av-to-audio.md`, `expo-av-to-video.md`, `react-navigation-to-expo-router.md` |
| Modules & config | `native-module.md`, `create-expo-module.md`, `config-plugin.md`, `module-config.md`, `lifecycle.md`, `setup.md` |
| Data & routes | `queries.md`, `expo-router-loaders.md` |

---

## Verification Checklist (قائمة التحقق)

- [ ] Tested on real device (not just simulator)
- [ ] Both light and dark mode
- [ ] Dynamic text size (smallest and largest)
- [ ] VoiceOver/TalkBack navigation
- [ ] All touch targets ≥ 44×44pt
- [ ] Smooth 60 FPS animations
- [ ] Offline state handled (cached content)
- [ ] Permission requests with explanations
- [ ] Empty states for all lists
- [ ] Error states for all async operations
- [ ] Loading states (skeleton, spinner)
- [ ] Keyboard avoidance in forms
- [ ] Bundle size reasonable (< 50MB)
- [ ] EAS build succeeds (iOS + Android)
- [ ] OTA update tested (if using EAS Update)

---

## Related Skills

- `$design-mobile` — for mobile UI/UX design
- `$testing-comprehensive` — for mobile testing
- `$backend-comprehensive` — for API design (mobile consumes)
- `$deployment-comprehensive` — for App Store / Play Store deployment
- `$security-comprehensive` — for mobile security
- `$code-engineering` — for mobile architecture
