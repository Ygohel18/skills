# Custom UI Component Library Guide

## Critical Rules

> **DO NOT install or use shadcn/ui.**
> **DO NOT copy shadcn source code.**
> **DO NOT import from `@/components/ui` if that package comes from a shadcn init.**
>
> All components must be **implemented from scratch** inside the project's own component system, following its existing conventions, utilities, and design tokens.

---

## Before Writing Any Component

1. **Inspect existing components first.** Read at least 2–3 existing components in the project's `components/ui/` directory.
2. **Match their exact patterns** for: TypeScript types, `cn()` / className handling, variant handling, `forwardRef`, composition, accessibility, and exports.
3. **Reuse what exists.** If there's already a `cn()` helper, a `buttonVariants` pattern, or a primitive — use it. Do not duplicate.
4. **One file per component.** Each component gets its own file. No mega-files.
5. **Named exports only.** No default exports.

---

## Standard Patterns to Follow

### className merging
Use the project's existing `cn()` utility (usually `lib/utils.ts`):
```ts
import { cn } from '@/lib/utils'
```

### forwardRef pattern
```tsx
const ComponentName = React.forwardRef<HTMLElement, ComponentProps>(
  ({ className, ...props }, ref) => (
    <element ref={ref} className={cn('base-classes', className)} {...props} />
  )
)
ComponentName.displayName = 'ComponentName'
```

### Variants (use class-variance-authority if already in project)
```ts
const componentVariants = cva('base-classes', {
  variants: {
    variant: { default: '...', destructive: '...', outline: '...' },
    size:    { sm: '...', md: '...', lg: '...' },
  },
  defaultVariants: { variant: 'default', size: 'md' },
})
```

### Accessibility
- Use semantic HTML (`<button>`, `<nav>`, `<dialog>`, `<form>`, `<table>`)
- Add `role` where semantic HTML isn't sufficient
- Add `aria-label`, `aria-labelledby`, `aria-describedby` where needed
- Add `aria-expanded`, `aria-selected`, `aria-checked`, `aria-disabled` for interactive states
- Keyboard: `Tab` to focus, `Enter`/`Space` to activate, `Escape` to close, arrow keys for lists

---

## Component Implementations

Below are reference implementations for all required components. Adapt them to match the **exact coding style and utilities** of the existing project.

---

### `alert`

```tsx
// components/ui/alert.tsx
import * as React from 'react'
import { cn } from '@/lib/utils'

interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'destructive' | 'success' | 'warning'
}

const variantClasses = {
  default:     'bg-background border text-foreground',
  destructive: 'border-destructive/50 text-destructive bg-destructive/10',
  success:     'border-green-500/50 text-green-700 bg-green-50 dark:bg-green-950/20 dark:text-green-400',
  warning:     'border-yellow-500/50 text-yellow-700 bg-yellow-50 dark:bg-yellow-950/20 dark:text-yellow-400',
}

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(
  ({ className, variant = 'default', ...props }, ref) => (
    <div ref={ref} role="alert"
         className={cn('relative w-full rounded-lg border p-4 [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg+div]:pl-7', variantClasses[variant], className)}
         {...props} />
  )
)
Alert.displayName = 'Alert'

const AlertTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h5 ref={ref} className={cn('mb-1 font-semibold leading-none tracking-tight', className)} {...props} />
  )
)
AlertTitle.displayName = 'AlertTitle'

const AlertDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('text-sm [&_p]:leading-relaxed', className)} {...props} />
  )
)
AlertDescription.displayName = 'AlertDescription'

export { Alert, AlertTitle, AlertDescription }
```

---

### `alert-dialog`

```tsx
// components/ui/alert-dialog.tsx
import * as React from 'react'
import { cn } from '@/lib/utils'

interface AlertDialogProps { open?: boolean; onOpenChange?: (open: boolean) => void; children: React.ReactNode }

const AlertDialogContext = React.createContext<{ open: boolean; setOpen: (v: boolean) => void }>({ open: false, setOpen: () => {} })

function AlertDialog({ open: controlledOpen, onOpenChange, children }: AlertDialogProps) {
  const [uncontrolled, setUncontrolled] = React.useState(false)
  const open    = controlledOpen ?? uncontrolled
  const setOpen = (v: boolean) => { setUncontrolled(v); onOpenChange?.(v) }
  return <AlertDialogContext.Provider value={{ open, setOpen }}>{children}</AlertDialogContext.Provider>
}

function AlertDialogTrigger({ children, asChild }: { children: React.ReactNode; asChild?: boolean }) {
  const { setOpen } = React.useContext(AlertDialogContext)
  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children as React.ReactElement<{ onClick?: () => void }>, { onClick: () => setOpen(true) })
  }
  return <button onClick={() => setOpen(true)}>{children}</button>
}

function AlertDialogContent({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  const { open, setOpen } = React.useContext(AlertDialogContext)
  React.useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false) }
    if (open) document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [open, setOpen])
  if (!open) return null
  return (
    <>
      <div className="fixed inset-0 z-50 bg-black/60 animate-in fade-in" onClick={() => setOpen(false)} />
      <div role="alertdialog" aria-modal="true"
           className={cn('fixed left-1/2 top-1/2 z-50 -translate-x-1/2 -translate-y-1/2 w-full max-w-lg rounded-xl bg-background shadow-lg border p-6 animate-in zoom-in-95', className)}
           {...props}>{children}</div>
    </>
  )
}

const AlertDialogHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('flex flex-col gap-2 text-center sm:text-left mb-4', className)} {...props} />
)
const AlertDialogFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('flex flex-col-reverse sm:flex-row sm:justify-end gap-2 mt-6', className)} {...props} />
)
const AlertDialogTitle = ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h2 className={cn('text-lg font-semibold', className)} {...props} />
)
const AlertDialogDescription = ({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) => (
  <p className={cn('text-sm text-muted-foreground', className)} {...props} />
)
function AlertDialogAction({ className, onClick, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  const { setOpen } = React.useContext(AlertDialogContext)
  return <button className={cn('inline-flex items-center justify-center rounded-lg bg-primary text-primary-foreground px-4 py-2 text-sm font-medium hover:bg-primary/90 transition-colors', className)}
                 onClick={(e) => { onClick?.(e); setOpen(false) }} {...props} />
}
function AlertDialogCancel({ className, onClick, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  const { setOpen } = React.useContext(AlertDialogContext)
  return <button className={cn('inline-flex items-center justify-center rounded-lg border bg-background px-4 py-2 text-sm font-medium hover:bg-muted transition-colors', className)}
                 onClick={(e) => { onClick?.(e); setOpen(false) }} {...props} />
}

export { AlertDialog, AlertDialogTrigger, AlertDialogContent, AlertDialogHeader, AlertDialogFooter, AlertDialogTitle, AlertDialogDescription, AlertDialogAction, AlertDialogCancel }
```

---

### `aspect-ratio`

```tsx
// components/ui/aspect-ratio.tsx
import * as React from 'react'
import { cn } from '@/lib/utils'

interface AspectRatioProps extends React.HTMLAttributes<HTMLDivElement> { ratio?: number }

const AspectRatio = React.forwardRef<HTMLDivElement, AspectRatioProps>(
  ({ ratio = 16 / 9, className, style, children, ...props }, ref) => (
    <div ref={ref} className={cn('relative w-full overflow-hidden', className)}
         style={{ paddingBottom: `${(1 / ratio) * 100}%`, ...style }} {...props}>
      <div className="absolute inset-0">{children}</div>
    </div>
  )
)
AspectRatio.displayName = 'AspectRatio'
export { AspectRatio }
```

---

### `breadcrumb`

```tsx
// components/ui/breadcrumb.tsx
import * as React from 'react'
import { ChevronRight, MoreHorizontal } from 'lucide-react'
import { cn } from '@/lib/utils'

const Breadcrumb = React.forwardRef<HTMLElement, React.ComponentPropsWithoutRef<'nav'> & { separator?: React.ReactNode }>(
  ({ ...props }, ref) => <nav ref={ref} aria-label="breadcrumb" {...props} />
)
Breadcrumb.displayName = 'Breadcrumb'

const BreadcrumbList = React.forwardRef<HTMLOListElement, React.ComponentPropsWithoutRef<'ol'>>(
  ({ className, ...props }, ref) => (
    <ol ref={ref} className={cn('flex flex-wrap items-center gap-1.5 break-words text-sm text-muted-foreground sm:gap-2.5', className)} {...props} />
  )
)
BreadcrumbList.displayName = 'BreadcrumbList'

const BreadcrumbItem = React.forwardRef<HTMLLIElement, React.ComponentPropsWithoutRef<'li'>>(
  ({ className, ...props }, ref) => <li ref={ref} className={cn('inline-flex items-center gap-1.5', className)} {...props} />
)
BreadcrumbItem.displayName = 'BreadcrumbItem'

const BreadcrumbLink = React.forwardRef<HTMLAnchorElement, React.ComponentPropsWithoutRef<'a'> & { asChild?: boolean }>(
  ({ className, ...props }, ref) => (
    <a ref={ref} className={cn('transition-colors hover:text-foreground', className)} {...props} />
  )
)
BreadcrumbLink.displayName = 'BreadcrumbLink'

const BreadcrumbPage = React.forwardRef<HTMLSpanElement, React.ComponentPropsWithoutRef<'span'>>(
  ({ className, ...props }, ref) => (
    <span ref={ref} role="link" aria-disabled="true" aria-current="page"
          className={cn('font-medium text-foreground', className)} {...props} />
  )
)
BreadcrumbPage.displayName = 'BreadcrumbPage'

const BreadcrumbSeparator = ({ children, className, ...props }: React.ComponentProps<'li'>) => (
  <li role="presentation" aria-hidden="true" className={cn('[&>svg]:h-3.5 [&>svg]:w-3.5', className)} {...props}>
    {children ?? <ChevronRight />}
  </li>
)
BreadcrumbSeparator.displayName = 'BreadcrumbSeparator'

const BreadcrumbEllipsis = ({ className, ...props }: React.ComponentProps<'span'>) => (
  <span role="presentation" aria-hidden="true" className={cn('flex h-9 w-9 items-center justify-center', className)} {...props}>
    <MoreHorizontal className="h-4 w-4" /><span className="sr-only">More</span>
  </span>
)
BreadcrumbEllipsis.displayName = 'BreadcrumbElipsis'

export { Breadcrumb, BreadcrumbList, BreadcrumbItem, BreadcrumbLink, BreadcrumbPage, BreadcrumbSeparator, BreadcrumbEllipsis }
```

---

### `checkbox`

```tsx
// components/ui/checkbox.tsx
import * as React from 'react'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  onCheckedChange?: (checked: boolean) => void
}

const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, onCheckedChange, onChange, ...props }, ref) => (
    <label className="inline-flex items-center cursor-pointer">
      <input
        type="checkbox" ref={ref}
        className="sr-only peer"
        onChange={(e) => { onChange?.(e); onCheckedChange?.(e.target.checked) }}
        {...props}
      />
      <span className={cn(
        'flex h-4 w-4 shrink-0 rounded-sm border border-primary shadow',
        'peer-focus-visible:outline-none peer-focus-visible:ring-2 peer-focus-visible:ring-ring peer-focus-visible:ring-offset-2',
        'peer-disabled:cursor-not-allowed peer-disabled:opacity-50',
        'peer-checked:bg-primary peer-checked:text-primary-foreground items-center justify-center',
        className
      )}>
        <Check className="h-3 w-3 hidden peer-checked:block" />
      </span>
    </label>
  )
)
Checkbox.displayName = 'Checkbox'
export { Checkbox }
```

---

### `collapsible`

```tsx
// components/ui/collapsible.tsx
import * as React from 'react'
import { cn } from '@/lib/utils'

interface CollapsibleProps { open?: boolean; onOpenChange?: (open: boolean) => void; defaultOpen?: boolean; children: React.ReactNode; className?: string }

const CollapsibleContext = React.createContext<{ open: boolean; toggle: () => void }>({ open: false, toggle: () => {} })

function Collapsible({ open: ctrl, onOpenChange, defaultOpen = false, children, className }: CollapsibleProps) {
  const [uncontrolled, setUncontrolled] = React.useState(defaultOpen)
  const open   = ctrl ?? uncontrolled
  const toggle = () => { const next = !open; setUncontrolled(next); onOpenChange?.(next) }
  return (
    <CollapsibleContext.Provider value={{ open, toggle }}>
      <div className={cn('', className)}>{children}</div>
    </CollapsibleContext.Provider>
  )
}

const CollapsibleTrigger = React.forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement>>(
  ({ onClick, children, ...props }, ref) => {
    const { open, toggle } = React.useContext(CollapsibleContext)
    return (
      <button ref={ref} type="button" aria-expanded={open} onClick={(e) => { toggle(); onClick?.(e) }} {...props}>
        {children}
      </button>
    )
  }
)
CollapsibleTrigger.displayName = 'CollapsibleTrigger'

const CollapsibleContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => {
    const { open } = React.useContext(CollapsibleContext)
    if (!open) return null
    return <div ref={ref} className={cn('animate-in fade-in-0 slide-in-from-top-1', className)} {...props}>{children}</div>
  }
)
CollapsibleContent.displayName = 'CollapsibleContent'

export { Collapsible, CollapsibleTrigger, CollapsibleContent }
```

---

### `progress`

```tsx
// components/ui/progress.tsx
import * as React from 'react'
import { cn } from '@/lib/utils'

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> { value?: number; max?: number }

const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value = 0, max = 100, ...props }, ref) => {
    const pct = Math.min(100, Math.max(0, (value / max) * 100))
    return (
      <div ref={ref} role="progressbar" aria-valuenow={value} aria-valuemin={0} aria-valuemax={max}
           className={cn('relative h-2 w-full overflow-hidden rounded-full bg-primary/20', className)} {...props}>
        <div className="h-full bg-primary transition-all duration-300 ease-in-out rounded-full"
             style={{ width: `${pct}%` }} />
      </div>
    )
  }
)
Progress.displayName = 'Progress'
export { Progress }
```

---

### `radio-group`

```tsx
// components/ui/radio-group.tsx
import * as React from 'react'
import { Circle } from 'lucide-react'
import { cn } from '@/lib/utils'

interface RadioGroupProps extends React.HTMLAttributes<HTMLDivElement> { value?: string; onValueChange?: (value: string) => void; defaultValue?: string }

const RadioGroupContext = React.createContext<{ value: string; onChange: (v: string) => void }>({ value: '', onChange: () => {} })

function RadioGroup({ value: ctrl, onValueChange, defaultValue = '', className, children, ...props }: RadioGroupProps) {
  const [uncontrolled, setUncontrolled] = React.useState(defaultValue)
  const value    = ctrl ?? uncontrolled
  const onChange = (v: string) => { setUncontrolled(v); onValueChange?.(v) }
  return (
    <RadioGroupContext.Provider value={{ value, onChange }}>
      <div role="radiogroup" className={cn('grid gap-2', className)} {...props}>{children}</div>
    </RadioGroupContext.Provider>
  )
}

interface RadioGroupItemProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type' | 'onChange'> { value: string }

const RadioGroupItem = React.forwardRef<HTMLInputElement, RadioGroupItemProps>(
  ({ className, value, ...props }, ref) => {
    const ctx = React.useContext(RadioGroupContext)
    const checked = ctx.value === value
    return (
      <label className="inline-flex items-center cursor-pointer gap-2">
        <input type="radio" ref={ref} value={value} checked={checked}
               onChange={() => ctx.onChange(value)} className="sr-only peer" {...props} />
        <span className={cn(
          'aspect-square h-4 w-4 rounded-full border border-primary',
          'peer-focus-visible:outline-none peer-focus-visible:ring-2 peer-focus-visible:ring-ring peer-focus-visible:ring-offset-2',
          'peer-disabled:cursor-not-allowed peer-disabled:opacity-50',
          'flex items-center justify-center', className
        )}>
          {checked && <Circle className="h-2.5 w-2.5 fill-primary text-primary" />}
        </span>
      </label>
    )
  }
)
RadioGroupItem.displayName = 'RadioGroupItem'
export { RadioGroup, RadioGroupItem }
```

---

### `select`

```tsx
// components/ui/select.tsx
import * as React from 'react'
import { ChevronDown } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SelectProps {
  value?: string; onValueChange?: (value: string) => void; defaultValue?: string
  open?: boolean; onOpenChange?: (open: boolean) => void; children: React.ReactNode
}
interface SelectContextValue { value: string; onChange: (v: string) => void; open: boolean; setOpen: (v: boolean) => void; triggerRef: React.RefObject<HTMLButtonElement> }

const SelectContext = React.createContext<SelectContextValue>({ value: '', onChange: () => {}, open: false, setOpen: () => {}, triggerRef: { current: null } })

function Select({ value: ctrl, onValueChange, defaultValue = '', open: ctrlOpen, onOpenChange, children }: SelectProps) {
  const [uncontrolledValue, setUncontrolledValue] = React.useState(defaultValue)
  const [uncontrolledOpen, setUncontrolledOpen]   = React.useState(false)
  const value   = ctrl ?? uncontrolledValue
  const open    = ctrlOpen ?? uncontrolledOpen
  const triggerRef = React.useRef<HTMLButtonElement>(null)
  const onChange = (v: string) => { setUncontrolledValue(v); onValueChange?.(v); setUncontrolledOpen(false); onOpenChange?.(false) }
  const setOpen  = (v: boolean) => { setUncontrolledOpen(v); onOpenChange?.(v) }
  return <SelectContext.Provider value={{ value, onChange, open, setOpen, triggerRef }}>{children}</SelectContext.Provider>
}

const SelectTrigger = React.forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement>>(
  ({ className, children, ...props }, ref) => {
    const { open, setOpen, triggerRef } = React.useContext(SelectContext)
    const mergedRef = (node: HTMLButtonElement | null) => {
      (triggerRef as React.MutableRefObject<HTMLButtonElement | null>).current = node
      if (typeof ref === 'function') ref(node); else if (ref) ref.current = node
    }
    return (
      <button ref={mergedRef} type="button" role="combobox" aria-expanded={open}
              onClick={() => setOpen(!open)}
              className={cn('flex h-9 w-full items-center justify-between rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50', className)}
              {...props}>
        {children}
        <ChevronDown className={cn('h-4 w-4 opacity-50 transition-transform', open && 'rotate-180')} />
      </button>
    )
  }
)
SelectTrigger.displayName = 'SelectTrigger'

const SelectValue = ({ placeholder, className }: { placeholder?: string; className?: string }) => {
  const { value } = React.useContext(SelectContext)
  return <span className={cn('block truncate', !value && 'text-muted-foreground', className)}>{value || placeholder}</span>
}

const SelectContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => {
    const { open, setOpen } = React.useContext(SelectContext)
    React.useEffect(() => {
      const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false) }
      if (open) document.addEventListener('keydown', onKey)
      return () => document.removeEventListener('keydown', onKey)
    }, [open, setOpen])
    if (!open) return null
    return (
      <>
        <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
        <div ref={ref} className={cn('absolute z-50 mt-1 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95', className)} {...props}>
          <div className="p-1">{children}</div>
        </div>
      </>
    )
  }
)
SelectContent.displayName = 'SelectContent'

interface SelectItemProps extends React.HTMLAttributes<HTMLDivElement> { value: string; disabled?: boolean }
const SelectItem = React.forwardRef<HTMLDivElement, SelectItemProps>(
  ({ className, children, value, disabled, ...props }, ref) => {
    const { onChange, value: selected } = React.useContext(SelectContext)
    const isSelected = selected === value
    return (
      <div ref={ref} role="option" aria-selected={isSelected}
           className={cn('relative flex w-full cursor-pointer select-none items-center rounded-sm py-1.5 px-2 text-sm outline-none hover:bg-accent hover:text-accent-foreground', isSelected && 'bg-accent text-accent-foreground', disabled && 'pointer-events-none opacity-50', className)}
           onClick={() => !disabled && onChange(value)} {...props}>
        {children}
      </div>
    )
  }
)
SelectItem.displayName = 'SelectItem'

const SelectLabel = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('px-2 py-1.5 text-xs font-semibold text-muted-foreground', className)} {...props} />
  )
)
SelectLabel.displayName = 'SelectLabel'

const SelectSeparator = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn('-mx-1 my-1 h-px bg-border', className)} {...props} />
)
SelectSeparator.displayName = 'SelectSeparator'

export { Select, SelectTrigger, SelectValue, SelectContent, SelectItem, SelectLabel, SelectSeparator }
```

---

### `slider`

```tsx
// components/ui/slider.tsx
import * as React from 'react'
import { cn } from '@/lib/utils'

interface SliderProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type' | 'value' | 'onChange'> {
  value?: number[]; defaultValue?: number[]; min?: number; max?: number; step?: number
  onValueChange?: (value: number[]) => void
}

const Slider = React.forwardRef<HTMLInputElement, SliderProps>(
  ({ className, value, defaultValue = [0], min = 0, max = 100, step = 1, onValueChange, ...props }, ref) => {
    const [internalValue, setInternalValue] = React.useState(defaultValue[0])
    const current = value ? value[0] : internalValue
    const pct     = ((current - min) / (max - min)) * 100
    return (
      <div className={cn('relative flex w-full touch-none select-none items-center', className)}>
        <div className="relative h-1.5 w-full grow overflow-hidden rounded-full bg-primary/20">
          <div className="absolute h-full bg-primary rounded-full" style={{ width: `${pct}%` }} />
        </div>
        <input
          ref={ref} type="range" min={min} max={max} step={step} value={current}
          onChange={(e) => { const v = Number(e.target.value); setInternalValue(v); onValueChange?.([v]) }}
          className="absolute inset-0 h-full w-full cursor-pointer opacity-0"
          aria-valuemin={min} aria-valuemax={max} aria-valuenow={current} {...props}
        />
        <div className="absolute h-4 w-4 rounded-full border-2 border-primary bg-background shadow transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
             style={{ left: `calc(${pct}% - 8px)` }} />
      </div>
    )
  }
)
Slider.displayName = 'Slider'
export { Slider }
```

---

### `input-otp`

```tsx
// components/ui/input-otp.tsx
import * as React from 'react'
import { cn } from '@/lib/utils'

interface InputOTPProps {
  length?: number; value?: string; onChange?: (value: string) => void
  onComplete?: (value: string) => void; className?: string; disabled?: boolean
}

function InputOTP({ length = 6, value = '', onChange, onComplete, className, disabled }: InputOTPProps) {
  const inputsRef = React.useRef<(HTMLInputElement | null)[]>([])

  const handleInput = (index: number, e: React.ChangeEvent<HTMLInputElement>) => {
    const char = e.target.value.replace(/\D/g, '').slice(-1)
    const arr  = value.split('')
    arr[index] = char
    const next = arr.slice(0, length).join('')
    onChange?.(next)
    if (char && index < length - 1) inputsRef.current[index + 1]?.focus()
    if (next.length === length) onComplete?.(next)
  }

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !value[index] && index > 0) inputsRef.current[index - 1]?.focus()
    if (e.key === 'ArrowLeft' && index > 0) inputsRef.current[index - 1]?.focus()
    if (e.key === 'ArrowRight' && index < length - 1) inputsRef.current[index + 1]?.focus()
  }

  const handlePaste = (e: React.ClipboardEvent) => {
    const text = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, length)
    onChange?.(text)
    if (text.length === length) { onComplete?.(text); inputsRef.current[length - 1]?.focus() }
    else inputsRef.current[text.length]?.focus()
    e.preventDefault()
  }

  return (
    <div className={cn('flex gap-2 items-center', className)}>
      {Array.from({ length }).map((_, i) => (
        <React.Fragment key={i}>
          <input
            ref={el => { inputsRef.current[i] = el }}
            type="text" inputMode="numeric" maxLength={1} value={value[i] ?? ''}
            onChange={(e) => handleInput(i, e)} onKeyDown={(e) => handleKeyDown(i, e)}
            onPaste={handlePaste} disabled={disabled}
            className="h-10 w-10 text-center text-base font-semibold rounded-md border border-input bg-background shadow-sm focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50 caret-transparent"
            aria-label={`Digit ${i + 1}`}
          />
          {i === Math.floor(length / 2) - 1 && (
            <div className="w-4 h-px bg-border" aria-hidden="true" />
          )}
        </React.Fragment>
      ))}
    </div>
  )
}

const InputOTPGroup = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('flex items-center gap-1', className)} {...props} />
)
const InputOTPSlot  = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('h-10 w-10 border rounded-md flex items-center justify-center text-sm', className)} {...props} />
)
const InputOTPSeparator = () => <div role="separator" className="text-muted-foreground">-</div>

export { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator }
```

---

### `toast`

```tsx
// components/ui/toast.tsx
import * as React from 'react'
import { X, CheckCircle, AlertCircle, Info } from 'lucide-react'
import { cn } from '@/lib/utils'

type ToastVariant = 'default' | 'success' | 'destructive' | 'warning'

interface ToastProps { id: string; title?: string; description?: string; variant?: ToastVariant; onDismiss: (id: string) => void; duration?: number }

const variantConfig: Record<ToastVariant, { icon: React.ReactNode; classes: string }> = {
  default:     { icon: <Info className="h-4 w-4" />,          classes: 'border bg-background text-foreground' },
  success:     { icon: <CheckCircle className="h-4 w-4" />,   classes: 'border-green-500/50 bg-green-50 text-green-800 dark:bg-green-950/30 dark:text-green-300' },
  destructive: { icon: <AlertCircle className="h-4 w-4" />,   classes: 'border-destructive/50 bg-destructive/10 text-destructive' },
  warning:     { icon: <AlertCircle className="h-4 w-4" />,   classes: 'border-yellow-500/50 bg-yellow-50 text-yellow-800 dark:bg-yellow-950/30 dark:text-yellow-300' },
}

function Toast({ id, title, description, variant = 'default', onDismiss, duration = 5000 }: ToastProps) {
  React.useEffect(() => {
    if (duration === Infinity) return
    const t = setTimeout(() => onDismiss(id), duration)
    return () => clearTimeout(t)
  }, [id, duration, onDismiss])

  const { icon, classes } = variantConfig[variant]
  return (
    <div role="alert" aria-live="assertive" aria-atomic="true"
         className={cn('group pointer-events-auto relative flex w-full items-start gap-3 overflow-hidden rounded-lg border p-4 shadow-lg transition-all animate-in slide-in-from-right-full', classes)}>
      <div className="mt-0.5 shrink-0">{icon}</div>
      <div className="flex-1 min-w-0">
        {title       && <p className="text-sm font-semibold leading-tight">{title}</p>}
        {description && <p className="text-sm opacity-90 mt-0.5 leading-snug">{description}</p>}
      </div>
      <button onClick={() => onDismiss(id)} aria-label="Dismiss"
              className="shrink-0 rounded-sm opacity-70 hover:opacity-100 focus:outline-none focus:ring-1 focus:ring-ring transition-opacity">
        <X className="h-4 w-4" />
      </button>
    </div>
  )
}

interface ToastState { id: string; title?: string; description?: string; variant?: ToastVariant; duration?: number }
interface ToastContextValue { toast: (opts: Omit<ToastState, 'id'>) => void; dismiss: (id: string) => void }

const ToastContext = React.createContext<ToastContextValue>({ toast: () => {}, dismiss: () => {} })

function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<ToastState[]>([])
  const dismiss = (id: string) => setToasts(t => t.filter(x => x.id !== id))
  const toast   = (opts: Omit<ToastState, 'id'>) => {
    const id = Math.random().toString(36).slice(2)
    setToasts(t => [...t, { id, ...opts }])
  }
  return (
    <ToastContext.Provider value={{ toast, dismiss }}>
      {children}
      <div className="fixed bottom-4 right-4 z-[100] flex flex-col gap-2 w-full max-w-sm">
        {toasts.map(t => <Toast key={t.id} {...t} onDismiss={dismiss} />)}
      </div>
    </ToastContext.Provider>
  )
}

function useToast() { return React.useContext(ToastContext) }

export { Toast, ToastProvider, useToast }
export type { ToastVariant }
```

---

### `table`

```tsx
// components/ui/table.tsx
import * as React from 'react'
import { cn } from '@/lib/utils'

const Table = React.forwardRef<HTMLTableElement, React.HTMLAttributes<HTMLTableElement>>(
  ({ className, ...props }, ref) => (
    <div className="relative w-full overflow-auto">
      <table ref={ref} className={cn('w-full caption-bottom text-sm', className)} {...props} />
    </div>
  )
)
Table.displayName = 'Table'
const TableHeader = React.forwardRef<HTMLTableSectionElement, React.HTMLAttributes<HTMLTableSectionElement>>(
  ({ className, ...props }, ref) => <thead ref={ref} className={cn('[&_tr]:border-b', className)} {...props} />
)
TableHeader.displayName = 'TableHeader'
const TableBody = React.forwardRef<HTMLTableSectionElement, React.HTMLAttributes<HTMLTableSectionElement>>(
  ({ className, ...props }, ref) => <tbody ref={ref} className={cn('[&_tr:last-child]:border-0', className)} {...props} />
)
TableBody.displayName = 'TableBody'
const TableFooter = React.forwardRef<HTMLTableSectionElement, React.HTMLAttributes<HTMLTableSectionElement>>(
  ({ className, ...props }, ref) => <tfoot ref={ref} className={cn('border-t bg-muted/50 font-medium [&>tr]:last:border-b-0', className)} {...props} />
)
TableFooter.displayName = 'TableFooter'
const TableRow = React.forwardRef<HTMLTableRowElement, React.HTMLAttributes<HTMLTableRowElement>>(
  ({ className, ...props }, ref) => (
    <tr ref={ref} className={cn('border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted', className)} {...props} />
  )
)
TableRow.displayName = 'TableRow'
const TableHead = React.forwardRef<HTMLTableCellElement, React.ThHTMLAttributes<HTMLTableCellElement>>(
  ({ className, ...props }, ref) => (
    <th ref={ref} className={cn('h-10 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0', className)} {...props} />
  )
)
TableHead.displayName = 'TableHead'
const TableCell = React.forwardRef<HTMLTableCellElement, React.TdHTMLAttributes<HTMLTableCellElement>>(
  ({ className, ...props }, ref) => (
    <td ref={ref} className={cn('p-4 align-middle [&:has([role=checkbox])]:pr-0', className)} {...props} />
  )
)
TableCell.displayName = 'TableCell'
const TableCaption = React.forwardRef<HTMLTableCaptionElement, React.HTMLAttributes<HTMLTableCaptionElement>>(
  ({ className, ...props }, ref) => <caption ref={ref} className={cn('mt-4 text-sm text-muted-foreground', className)} {...props} />
)
TableCaption.displayName = 'TableCaption'

export { Table, TableHeader, TableBody, TableFooter, TableHead, TableRow, TableCell, TableCaption }
```

---

### `toggle`

```tsx
// components/ui/toggle.tsx
import * as React from 'react'
import { cn } from '@/lib/utils'

interface ToggleProps extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'onClick'> {
  pressed?: boolean; defaultPressed?: boolean; onPressedChange?: (pressed: boolean) => void; variant?: 'default' | 'outline'; size?: 'sm' | 'md' | 'lg'
}

const Toggle = React.forwardRef<HTMLButtonElement, ToggleProps>(
  ({ className, pressed: ctrl, defaultPressed = false, onPressedChange, variant = 'default', size = 'md', children, ...props }, ref) => {
    const [uncontrolled, setUncontrolled] = React.useState(defaultPressed)
    const pressed  = ctrl ?? uncontrolled
    const toggle   = () => { const next = !pressed; setUncontrolled(next); onPressedChange?.(next) }
    return (
      <button ref={ref} type="button" role="switch" aria-pressed={pressed} onClick={toggle}
              className={cn(
                'inline-flex items-center justify-center rounded-md font-medium ring-offset-background transition-colors',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
                'disabled:pointer-events-none disabled:opacity-50',
                variant === 'outline' ? 'border border-input bg-transparent hover:bg-accent hover:text-accent-foreground' : 'hover:bg-muted hover:text-muted-foreground',
                pressed && 'bg-accent text-accent-foreground',
                size === 'sm' ? 'h-8 px-2.5 text-xs' : size === 'lg' ? 'h-11 px-5 text-base' : 'h-9 px-3 text-sm',
                className
              )}
              {...props}>{children}</button>
    )
  }
)
Toggle.displayName = 'Toggle'
export { Toggle }
```

---

### `toggle-group`

```tsx
// components/ui/toggle-group.tsx
import * as React from 'react'
import { cn } from '@/lib/utils'
import { Toggle } from './toggle'

interface ToggleGroupProps extends React.HTMLAttributes<HTMLDivElement> {
  type: 'single' | 'multiple'; value?: string | string[]; defaultValue?: string | string[]
  onValueChange?: (value: string | string[]) => void; variant?: 'default' | 'outline'; size?: 'sm' | 'md' | 'lg'
}

function ToggleGroup({ type, value: ctrl, defaultValue, onValueChange, variant, size, className, children, ...props }: ToggleGroupProps) {
  const [uncontrolled, setUncontrolled] = React.useState<string | string[]>(defaultValue ?? (type === 'multiple' ? [] : ''))
  const value = ctrl ?? uncontrolled

  const handleChange = (item: string) => {
    let next: string | string[]
    if (type === 'single') {
      next = (value as string) === item ? '' : item
    } else {
      const arr = (value as string[])
      next = arr.includes(item) ? arr.filter(v => v !== item) : [...arr, item]
    }
    setUncontrolled(next); onValueChange?.(next)
  }

  return (
    <div role="group" className={cn('flex items-center gap-1', className)} {...props}>
      {React.Children.map(children, (child) => {
        if (!React.isValidElement(child)) return child
        const itemValue = (child.props as { value?: string }).value ?? ''
        const isPressed = type === 'single' ? value === itemValue : (value as string[]).includes(itemValue)
        return React.cloneElement(child as React.ReactElement<{ pressed?: boolean; onPressedChange?: (p: boolean) => void; variant?: string; size?: string }>, {
          pressed: isPressed, onPressedChange: () => handleChange(itemValue), variant, size,
        })
      })}
    </div>
  )
}

interface ToggleGroupItemProps extends React.ComponentPropsWithoutRef<typeof Toggle> { value: string }
const ToggleGroupItem = React.forwardRef<HTMLButtonElement, ToggleGroupItemProps>(
  ({ value, ...props }, ref) => <Toggle ref={ref} {...props} />
)
ToggleGroupItem.displayName = 'ToggleGroupItem'

export { ToggleGroup, ToggleGroupItem }
```

---

### `pagination`

```tsx
// components/ui/pagination.tsx
import * as React from 'react'
import { ChevronLeft, ChevronRight, MoreHorizontal } from 'lucide-react'
import { cn } from '@/lib/utils'

const Pagination  = ({ className, ...props }: React.ComponentProps<'nav'>) => (
  <nav role="navigation" aria-label="pagination" className={cn('mx-auto flex w-full justify-center', className)} {...props} />
)
const PaginationContent = React.forwardRef<HTMLUListElement, React.ComponentProps<'ul'>>(
  ({ className, ...props }, ref) => <ul ref={ref} className={cn('flex flex-row items-center gap-1', className)} {...props} />
)
PaginationContent.displayName = 'PaginationContent'
const PaginationItem = React.forwardRef<HTMLLIElement, React.ComponentProps<'li'>>(
  ({ className, ...props }, ref) => <li ref={ref} className={cn('', className)} {...props} />
)
PaginationItem.displayName = 'PaginationItem'
interface PaginationLinkProps extends React.ComponentProps<'a'> { isActive?: boolean; size?: 'sm' | 'md' }
const PaginationLink = ({ className, isActive, size = 'md', ...props }: PaginationLinkProps) => (
  <a aria-current={isActive ? 'page' : undefined}
     className={cn('inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors',
       'focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring cursor-pointer',
       isActive ? 'border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground' : 'hover:bg-accent hover:text-accent-foreground',
       size === 'sm' ? 'h-8 w-8' : 'h-9 w-9', className)} {...props} />
)
PaginationLink.displayName = 'PaginationLink'
const PaginationPrevious = ({ className, ...props }: React.ComponentProps<typeof PaginationLink>) => (
  <PaginationLink aria-label="Go to previous page" size="md" className={cn('gap-1 pl-2.5', className)} {...props}>
    <ChevronLeft className="h-4 w-4" /><span>Previous</span>
  </PaginationLink>
)
PaginationPrevious.displayName = 'PaginationPrevious'
const PaginationNext = ({ className, ...props }: React.ComponentProps<typeof PaginationLink>) => (
  <PaginationLink aria-label="Go to next page" size="md" className={cn('gap-1 pr-2.5', className)} {...props}>
    <span>Next</span><ChevronRight className="h-4 w-4" />
  </PaginationLink>
)
PaginationNext.displayName = 'PaginationNext'
const PaginationEllipsis = ({ className, ...props }: React.ComponentProps<'span'>) => (
  <span aria-hidden className={cn('flex h-9 w-9 items-center justify-center', className)} {...props}>
    <MoreHorizontal className="h-4 w-4" /><span className="sr-only">More pages</span>
  </span>
)
PaginationEllipsis.displayName = 'PaginationEllipsis'

export { Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationPrevious, PaginationNext, PaginationEllipsis }
```

---

### Remaining Components (Architecture Notes)

For the remaining components, follow the same pattern. Here are the implementation approach for each:

#### `combobox`
A combination of `Select` + search input. Open a popover, render a text input filtered list of `SelectItem`-like options. State: `open`, `inputValue` (filter), `value` (selected). Filter options by `inputValue.toLowerCase()`.

#### `command`
A searchable list/command palette. Structure: `Command > CommandInput + CommandList > CommandGroup > CommandItem`. State: `inputValue` (filter). Filter `CommandItem` children by matching their `value` prop against `inputValue`.

#### `context-menu`
Right-click triggered menu. On `onContextMenu`, `preventDefault()` and store `{x, y}` coords. Render a `position: fixed` menu at those coords. Close on `Escape`, click-outside, or item selection.

#### `drawer`
A Sheet-style panel that slides in from bottom (on mobile) or side (on desktop). Identical to the existing `Sheet` but with `side="bottom"` default and swipe-to-dismiss gesture support via touch events (`touchstart`/`touchmove`/`touchend`).

#### `form`
Wraps a `<form>` element. Pairs with `react-hook-form` or a minimal context providing `register`, `error`, `formState`. Sub-components: `FormField`, `FormItem`, `FormLabel`, `FormControl`, `FormMessage`, `FormDescription`. `FormMessage` reads from context error for the named field.

#### `hover-card`
A popover that appears on mouse hover (with 300ms delay). State: `open`, managed by `onMouseEnter`/`onMouseLeave` with `setTimeout`. Structure: `HoverCard > HoverCardTrigger + HoverCardContent`.

#### `navigation-menu`
Horizontal or vertical navigation with optional mega-menu dropdowns. Structure: `NavigationMenu > NavigationMenuList > NavigationMenuItem > NavigationMenuTrigger + NavigationMenuContent`. Trigger shows content on hover (desktop) or click (mobile). `NavigationMenuLink` is a styled `<a>`.

#### `menubar`
A horizontal bar of menu triggers, each opening a dropdown. Structure: `Menubar > MenubarMenu > MenubarTrigger + MenubarContent > MenubarItem | MenubarSeparator | MenubarSub`. State: `activeMenu` (which trigger is open). Only one menu open at a time.

#### `resizable`
Resizable panel layout. Structure: `ResizablePanelGroup > ResizablePanel + ResizableHandle`. Use CSS flex + drag event handlers on `ResizableHandle` to adjust panel sizes as percentages. State stored in `ResizablePanelGroup`.

#### `calendar`
A date picker calendar. State: `currentMonth`, `currentYear`, `selectedDate`. Render a 7-column grid of day cells. Navigation: Previous/Next month buttons. Day cells: highlight today, disable past/future if min/max props set, show selected with primary color. Use vanilla JS `Date` — no external date library required.

---

## Updated Barrel Export

After creating all components, update `index.ts` (or the project's barrel file) to:

```ts
export * from './accordion';
export * from './alert';
export * from './alert-dialog';
export * from './aspect-ratio';
export * from './avatar';
export * from './badge';
export * from './breadcrumb';
export * from './button';
export * from './calendar';
export * from './card';
export * from './checkbox';
export * from './collapsible';
export * from './combobox';
export * from './command';
export * from './context-menu';
export * from './dialog';
export * from './drawer';
export * from './dropdown-menu';
export * from './form';
export * from './hover-card';
export * from './input';
export * from './input-otp';
export * from './label';
export * from './menubar';
export * from './navigation-menu';
export * from './pagination';
export * from './popover';
export * from './progress';
export * from './radio-group';
export * from './resizable';
export * from './scroll-area';
export * from './select';
export * from './separator';
export * from './sheet';
export * from './skeleton';
export * from './slider';
export * from './switch';
export * from './table';
export * from './tabs';
export * from './textarea';
export * from './toast';
export * from './toggle';
export * from './toggle-group';
export * from './tooltip';
```

---

## Implementation Checklist

Before each component is marked done:

- [ ] Inspected 2+ existing components for pattern consistency
- [ ] Matches existing file naming and export style
- [ ] Uses project's `cn()` (not custom merging)
- [ ] `forwardRef` used where a DOM element is exposed
- [ ] `displayName` set on every component
- [ ] TypeScript props interface exported alongside component
- [ ] Keyboard navigation implemented (Tab, Enter, Space, Escape, Arrow keys where applicable)
- [ ] ARIA attributes correct (role, aria-expanded, aria-selected, aria-label, aria-hidden)
- [ ] Controlled + uncontrolled mode supported
- [ ] No hardcoded colours (only `className` tokens from design system)
- [ ] Works on mobile (touch-friendly, correct tap target size)
- [ ] No shadcn imports, no external component library imports
- [ ] Named exports only (no default exports)
