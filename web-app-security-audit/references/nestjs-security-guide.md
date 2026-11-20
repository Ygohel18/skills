# NestJS Security Audit Guide

A security manual covering vulnerability vectors and hardening procedures for NestJS applications, DTO validation, guard architectures, and ORM query safety.

---

## 1. DTO Over-Posting & Missing `whitelist: true`

NestJS relies on `ValidationPipe` and `class-validator` to inspect incoming HTTP payloads. By default, `ValidationPipe` validates decorated properties but does **not strip or reject un-decorated properties** sent by the client.

### Vulnerable Pattern
```typescript
// DTO
export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  name: string;
}

// Controller
@Post()
create(@Body() dto: CreateUserDto) {
  // ❌ VULNERABLE: If client sends {"email": "...", "name": "...", "isAdmin": true},
  // the 'isAdmin' property passes directly into the database query!
  return this.usersService.create(dto);
}
```

### Remediated Pattern
Enforce `whitelist: true` and `forbidNonWhitelisted: true` globally in `main.ts`:

```typescript
// main.ts
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,               // Strips properties without decorators
      forbidNonWhitelisted: true,     // Throws 400 Bad Request if extra fields present
      transform: true,               // Automatically casts primitives to DTO types
      transformOptions: {
        enableImplicitConversion: false,
      },
    }),
  );

  await app.listen(3000);
}
```

---

## 2. Missing Guards & Broken Access Control

A common failure mode in NestJS is omitting `@UseGuards(AuthGuard)` on newly created controller routes, leaving sensitive APIs publicly accessible.

### Recommended Defense: Global Guards with `@Public()` Bypass
Apply authentication globally across all routes by default, requiring developers to explicitly opt-out for public endpoints:

```typescript
// app.module.ts
import { APP_GUARD } from '@nestjs/core';

@Module({
  providers: [
    {
      provide: APP_GUARD,
      useClass: JwtAuthGuard, // Protects EVERY route by default
    },
  ],
})
export class AppModule {}
```

Create a custom `@Public()` decorator for unauthenticated endpoints:
```typescript
// public.decorator.ts
import { SetMetadata } from '@nestjs/common';
export const IS_PUBLIC_KEY = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);

// auth.controller.ts
@Controller('auth')
export class AuthController {
  @Public() // Explicitly marked as public
  @Post('login')
  login(@Body() loginDto: LoginDto) { ... }
}
```

---

## 3. Raw SQL Concatenation in TypeORM & Prisma

Even when using TypeORM, Prisma, or Sequelize, calling raw query helpers with template strings introduces SQL injection vulnerabilities.

### Vulnerable Pattern (TypeORM)
```typescript
// ❌ VULNERABLE: Direct string interpolation into raw query
const users = await this.userRepository.query(
  `SELECT * FROM users WHERE organization_id = '${orgId}' AND status = '${status}'`
);
```

### Remediated Pattern
```typescript
// ✅ SECURE: Parameterized positional bindings ($1, $2 or ?)
const users = await this.userRepository.query(
  'SELECT * FROM users WHERE organization_id = $1 AND status = $2',
  [orgId, status]
);
```

---

## 4. Rate Limiting with `ThrottlerModule`

Prevent brute-force attacks on authentication routes by registering the official NestJS Throttler module:

```typescript
// app.module.ts
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';

@Module({
  imports: [
    ThrottlerModule.forRoot([{
      ttl: 60000, // 60 seconds
      limit: 10,   // 10 requests per TTL window
    }]),
  ],
  providers: [
    {
      provide: APP_GUARD,
      useClass: ThrottlerGuard,
    },
  ],
})
export class AppModule {}
```
