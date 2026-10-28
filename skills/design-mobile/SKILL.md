---
name: design-mobile
description: Mobile app design skill for iOS and Android — native UI patterns, platform guidelines, gestures, navigation, typography, accessibility, Expo/React Native design, responsive mobile layouts, and modern mobile UX. Use when building or reviewing any mobile app interface.
---

# Mobile Design — Complete Skill

## Overview

Covers **iOS and Android design**: platform-specific patterns, navigation, gestures, typography, accessibility, and modern trends. Merges `building-native-ui`, `expo-ui-swiftui`, `expo-ui-jetpack-compose`, `engineering-mobile-app-builder`, `react-native-best-practices`, `expo-tailwind-setup`, and `native-data-fetching`.

---

## 1. Platform Guidelines (إرشادات المنصة)

### 1.1 iOS (Human Interface Guidelines)
- **Navigation:** push/pop (UINavigationController), tab bar, modal sheets
- **Typography:** SF Pro (San Francisco) — New York (serif) for reading
- **Grid:** 4pt grid, margins: 16pt (standard), 20pt (large)
- **Colors:** system colors (blue, green, red, orange, purple, pink, teal, indigo, gray)
- **Touch targets:** minimum 44×44pt
- **Back gesture:** swipe from left edge
- **Safe areas:** notch, home indicator (use `safe-area-inset`)
- **Dark mode:** `UIColor { traitCollection }` system adaptation

### 1.2 Android (Material Design 3)
- **Navigation:** bottom navigation, navigation drawer, top app bar, back button
- **Typography:** Roboto (system), Google Sans (branding)
- **Grid:** 4dp grid, margins: 16dp
- **Colors:** dynamic color (Material You), tonal palettes
- **Touch targets:** minimum 48×48dp
- **Back button:** system back (predictive back in Android 14)
- **Elevation:** shadows represent depth and interaction priority
- **Ripple effect:** touch feedback on all interactive elements

### 1.3 Cross-Platform (React Native / Expo)
- **Try Expo Go first** for rapid prototyping
- Use `useWindowDimensions()` instead of `Dimensions.get()`
- `boxShadow` for cross-platform shadows (not legacy shadow/elevation)
- `expo-image` for better image loading and SF Symbols
- Platform-specific code: `.ios.tsx` / `.android.tsx`

---

## 2. Mobile Navigation (التنقل)

### 2.1 Navigation Patterns
| Pattern | When to Use | Platform |
|---------|-------------|----------|
| **Tab Bar** | 3-5 top-level destinations | iOS (bottom), Android (bottom) |
| **Bottom Navigation** | 3-5 top-level destinations | Material Design |
| **Navigation Drawer** | Many destinations, infrequent access | Android |
| **Stack Navigation** | Hierarchical drill-down | Both |
| **Modal Sheets** | Focused tasks, quick actions | iOS (form sheet), Android (bottom sheet) |
| **Full-Screen Modal** | Multi-step flows | Both |
| **Swipe Actions** | List item actions (delete, archive) | Both |

### 2.2 Tab Bar Rules
- Max 5 tabs (iOS), 5 max (Material)
- Active state: filled icon + label color change
- Badge: red dot with count for notifications
- Safe area: above home indicator on iOS

### 2.3 Stack Navigation
- Push: slide from right (iOS), fade+slide (Android)
- Pop: swipe from left edge (iOS), back button (Android)
- Transition: 300ms (iOS), 200-300ms (Android)

### 2.4 Gestures
- **Swipe:** list actions, navigation between screens
- **Pull to refresh:** standard pattern for lists
- **Long press:** contextual menu (300-500ms delay)
- **Pinch to zoom:** images, maps
- **Double tap:** zoom, like (social apps)

---

## 3. Mobile Typography (الطباعة)

### 3.1 Type Scale
| Style | Size | Weight | Line Height |
|-------|------|--------|-------------|
| Large Title | 34pt | 700 | 41pt |
| Title 1 | 28pt | 700 | 34pt |
| Title 2 | 22pt | 700 | 28pt |
| Title 3 | 20pt | 600 | 25pt |
| Headline | 17pt | 600 | 22pt |
| Body | 17pt | 400 | 22pt |
| Callout | 16pt | 400 | 21pt |
| Subheadline | 15pt | 400 | 20pt |
| Footnote | 13pt | 400 | 18pt |
| Caption 1 | 12pt | 400 | 16pt |
| Caption 2 | 11pt | 400 | 13pt |

### 3.2 Rules
- **Minimum text size:** 12sp (Android), 11pt (iOS)
- **Body text:** 16-17pt for comfortable reading
- **Line height:** 1.3-1.5× font size
- **Never truncate:** critical text (numbers, names, dates)
- **Line length:** 40-70 characters max
- **Dynamic type:** support system text size (iOS: `UIFontMetrics`, Android: `sp`)

---

## 4. Mobile Components (المكونات)

### 4.1 Common Components
| Component | iOS | Android (Material) |
|-----------|-----|---------------------|
| Button | UIButton (filled, tinted, gray) | Elevated, filled, tonal, outlined, text |
| List | UITableView (grouped, inset) | RecyclerView (list, card) |
| Input | UITextField | TextField (filled, outlined) |
| Toggle | UISwitch | Switch |
| Slider | UISlider | Slider |
| Picker | Wheel picker / dropdown | Dropdown menu |
| Tab bar | UITabBar | BottomNavigationView |
| Search | UISearchBar | SearchBar |
| Toast | N/A (use custom) | Snackbar |

### 4.2 List Patterns
- **Standard:** icon + title + subtitle + chevron
- **Action:** swipe left → delete/archive/share
- **Grouped:** section headers with grouped items
- **Card:** image + title + description + actions
- **Infinite scroll:** load more on scroll (with loading indicator)

### 4.3 Form Patterns
- **Single column** always (mobile)
- **Labels:** above inputs (not floating only)
- **Keyboard type:** match input (numeric, email, phone)
- **Keyboard avoidance:** scroll form when keyboard appears
- **Validation:** inline below field, color change
- **Submit:** sticky bottom button or form action

---

## 5. Mobile Layout (التنسيق)

### 5.1 Safe Areas
```jsx
// Expo / React Native
import { useSafeAreaInsets } from 'react-native-safe-area-context';

const insets = useSafeAreaInsets();
<View style={{ paddingTop: insets.top, paddingBottom: insets.bottom }} />
```

### 5.2 Screen Density
- **iPhone SE:** 375×667pt (smallest)
- **iPhone 14:** 390×844pt
- **iPhone 14 Pro Max:** 430×932pt
- **Android:** 360×640dp (common), varies widely

### 5.3 Touch Targets
- **Minimum:** 44×44pt (iOS), 48×48dp (Android)
- **Preferred:** 48×48pt for thumb-friendly zones
- **Spacing:** 8pt minimum between adjacent touch targets

### 5.4 Thumb Zones
- **Best zone:** bottom half of screen (natural thumb reach)
- **Primary actions:** bottom 1/3 (especially on large phones)
- **Destructive actions:** away from primary zone

---

## 6. Mobile Design System (نظام التصميم)

### 6.1 Color System
```css
/* Light mode */
--primary: #007AFF;        /* iOS blue / Android blue */
--background: #FFFFFF;
--surface: #F2F2F7;
--text-primary: #000000;
--text-secondary: #8E8E93;
--separator: #C6C6C8;
--success: #34C759;
--error: #FF3B30;
--warning: #FF9500;

/* Dark mode */
--primary: #0A84FF;
--background: #000000;
--surface: #1C1C1E;
--text-primary: #FFFFFF;
--text-secondary: #8E8E93;
```

### 6.2 Dark Mode
- System-wide toggle (follow OS setting)
- Pure black (#000) for OLED (iOS) or dark gray (#121212) for Android
- Reduce contrast slightly in dark mode
- Test both modes for every screen

### 6.3 Iconography
- **iOS:** SF Symbols (system), custom icons (app-specific)
- **Android:** Material Icons (system), custom
- **Size:** 24×24dp standard, 18×18dp small, 28×28dp large
- **Style:** filled (active), outlined (inactive)

---

## 7. Motion & Animation (الحركة)

### 7.1 Principles
- **Duration:** 250-350ms (standard), 150-200ms (fast), 500ms+ (complex)
- **Easing:** `cubic-bezier(0.2, 0, 0, 1)` (Material), `ease-out` (iOS)
- **Purpose:** indicate navigation, confirm action, show loading, delight

### 7.2 Common Patterns
| Animation | Duration | Use |
|-----------|----------|-----|
| Page push/pop | 300ms | Stack navigation |
| Modal present/dismiss | 300ms | Modal sheets |
| Fade in | 200ms | Content loading |
| Slide up | 250ms | Bottom sheet |
| Scale up | 200ms | Button press feedback |
| Skeleton | 1.5s loop | Content loading |
| Pull to refresh | 200ms | List refresh |

### 7.3 Platform-Specific
- **iOS:** spring physics (natural, bouncy)
- **Android:** standard easing (predictable, smooth)
- **Haptics:** light impact (button press), medium (selection), success/error patterns

---

## 8. Mobile UX Patterns (أنماط تجربة المستخدم)

### 8.1 Onboarding
- **3-5 screens max:** value proposition → features → permissions → CTA
- **Skip option:** always available
- **Progress indicator:** dots or progress bar
- **Permission requests:** explain WHY before requesting

### 8.2 Empty States
- Illustration or icon
- Clear message
- Call-to-action button
- Examples: "No results", "Your cart is empty", "No notifications"

### 8.3 Loading States
- **Skeleton screens** (preferred over spinners)
- **Progress bars** for measurable operations
- **Pull-to-refresh** for lists
- **Optimistic UI** for actions (update immediately, rollback on error)

### 8.4 Error States
- **Inline:** field-level validation errors
- **Full-screen:** critical errors with retry button
- **Toast/snackbar:** transient errors (3-5 seconds)
- **Offline:** cached content + "You're offline" banner

### 8.5 Notifications
- **Push:** permission request with explanation
- **In-app:** badge, banner, or inbox
- **Settings:** granular control (per category)

---

## 9. Accessibility (إمكانية الوصول)

### 9.1 Checklist
- [ ] All touch targets ≥ 44×44pt
- [ ] Text supports Dynamic Type / font scaling
- [ ] Color contrast ≥ 4.5:1
- [ ] All images have alt text (accessibilityLabel)
- [ ] Screen reader: VoiceOver (iOS) / TalkBack (Android)
- [ ] Focus order follows visual order
- [ ] Haptic feedback for important actions
- [ ] Reduced motion respected
- [ ] No color-only information
- [ ] Forms have proper labels

### 9.2 Screen Reader
- **iOS VoiceOver:** `accessibilityLabel`, `accessibilityHint`, `accessibilityTraits`
- **Android TalkBack:** `contentDescription`, `accessibilityRole`
- **Test:** enable screen reader and navigate full app

---

## 10. Performance (الأداء)

### 10.1 Key Metrics
- **TTI (Time to Interactive):** < 2s
- **Frame rate:** 60 FPS (16.67ms per frame)
- **App size:** minimize bundle
- **Memory:** no leaks, proper cleanup

### 10.2 Optimization
- Use `FlatList` (not ScrollView) for long lists
- Memoize expensive components (`React.memo`, `useMemo`, `useCallback`)
- Lazy load screens and images
- Reduce re-renders (proper key props, avoid anonymous functions in props)
- Image caching and compression
- Hermes engine for React Native

---

## 11. Expo Native UI Components (مكونات أصلية)

### 11.1 Expo UI — SwiftUI (iOS)
```bash
npx expo install @expo/ui
```
```tsx
import { Host, SwiftUIButton } from '@expo/ui/swift-ui';

export default function Screen() {
  return (
    <Host>                                 {/* every SwiftUI tree needs Host */}
      <SwiftUIButton title="Tap me" action={onPress} />
    </Host>
  );
}
```
- ⚠️ **Every SwiftUI tree must be wrapped in `Host`** — otherwise nothing renders
- Embed React Native components inside a SwiftUI tree with `RNHostView`
- Read the package `.d.ts` and component docs before use — modifiers change between SDK versions

### 11.2 Expo UI — Jetpack Compose (Android)
```tsx
import { Host, Button } from '@expo/ui/jetpack-compose';
import { composeModifiers } from '@expo/ui/jetpack-compose/modifiers';

<Host>
  <Button title="Tap me" modifiers={[composeModifiers.padding(16)]} onPress={onPress} />
</Host>
```
- ⚠️ **Wrap every Compose tree in `Host`** (same rule as SwiftUI)
- Long lists → `LazyColumn`; icons → `Icon` with local XML files
- Read the component's `.d.ts` before using modifiers — API is SDK-version specific

### 11.3 NativeWind v5 + Tailwind v4 (cross-platform styling)
```bash
npm i nativewind react-native-css tailwindcss @tailwindcss/postcss
```
```tsx
// src/tw/index.tsx — wrapped components with className support
import { styled } from 'nativewind';
export const View = styled(NativeView);
```
- **No `babel.config.js` changes needed** — react-native-css handles transform at runtime
- Output lives in `src/tw/` (wrapped `View`, `Text`, `Image`, `animated`)
- Use `className` everywhere; falls back to `style` for one-offs
- Web target: same `className` works on React Native Web — one codebase, three platforms

### 11.4 When to Use Which
| Need | Use |
|------|-----|
| Native look (SwiftUI/Compose) | `@expo/ui` with `Host` |
| Cross-platform + fast iteration | NativeWind v5 |
| Custom drawing / animation | Reanimated + Skia |
| Standard RN components | Built-in `View`/`Text`/`Pressable` |

---

## 12. Verification Checklist (قائمة التحقق)

- [ ] Tested on real device (not just simulator)
- [ ] Both light and dark mode
- [ ] Dynamic text size (smallest and largest)
- [ ] VoiceOver/TalkBack navigation
- [ ] All touch targets accessible
- [ ] No layout breaks on smallest screen (iPhone SE)
- [ ] No layout breaks on largest screen (tablet)
- [ ] Smooth 60 FPS animations
- [ ] Offline state handled
- [ ] Permission requests with explanations
- [ ] Empty states for all lists
- [ ] Error states for all async operations
- [ ] Loading states (skeleton, spinner)
- [ ] Keyboard avoidance in forms

---

## Related Skills

- `$design-web` — for web interface design
- `$design-desktop` — for desktop application design
- `$design-figma` — for Figma design work
- `$mobile-development` — for Expo/React Native development
- `$testing-web` — for testing mobile web
- `$testing-desktop` — for testing desktop apps
