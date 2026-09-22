# Framer Motion Patterns

These concise implementation patterns support the `framer-motion` skill directives.

## 1. Typed Variants

```tsx
import type { Variants } from "framer-motion";

export const fadeUpVariant: Variants = {
  hidden: { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } },
};
```

## 2. Staggered Children

```tsx
export const containerVariant: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};
// Use with fadeUpVariant on children
```

## 3. AnimatePresence Modal

```tsx
import { motion, AnimatePresence } from "framer-motion";

<AnimatePresence>
  {isOpen && (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.2 }}
      role="dialog"
      aria-modal="true"
    >
      {/* Modal Content */}
    </motion.div>
  )}
</AnimatePresence>
```

## 4. Reduced-Motion Handling

```tsx
import { motion, useReducedMotion } from "framer-motion";

export function AccessibleReveal({ children }) {
  const prefersReducedMotion = useReducedMotion();
  
  return (
    <motion.div
      initial={prefersReducedMotion ? { opacity: 1 } : { opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
    >
      {children}
    </motion.div>
  );
}
```

## 5. Next.js Client Animation Wrapper

```tsx
"use client";
import { motion } from "framer-motion";
import type { ReactNode } from "react";

export function FadeIn({ children }: { children: ReactNode }) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {children}
    </motion.div>
  );
}
```

## 6. Scroll Reveal

```tsx
import { motion } from "framer-motion";

<motion.div
  initial={{ opacity: 0, y: 24 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px" }}
  transition={{ duration: 0.5 }}
>
  Revealed Content
</motion.div>
```

## 7. Shared Layout Transition

```tsx
import { motion } from "framer-motion";

<motion.div layoutId="underline" className="absolute bottom-0 h-1 bg-gold w-full" />
```

## 8. Accessible Drawer

```tsx
import { motion, AnimatePresence } from "framer-motion";

<AnimatePresence>
  {isOpen && (
    <>
      <motion.div
        key="backdrop"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50"
        onClick={onClose}
      />
      <motion.div
        key="drawer"
        initial={{ x: "100%" }}
        animate={{ x: 0 }}
        exit={{ x: "100%" }}
        transition={{ type: "tween", duration: 0.3 }}
        className="fixed right-0 top-0 h-full w-80 bg-white"
        role="dialog"
      >
        {/* Drawer Content */}
      </motion.div>
    </>
  )}
</AnimatePresence>
```
