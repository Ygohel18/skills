# Framework-Specific Testing Patterns & Idioms

> Companion reference for `testing-strategy`.
> Practical implementation examples showing how to write clean, parameterized, and well-isolated tests across major frameworks.

---

## 1. Python (`pytest`)

`pytest` is the de-facto Python standard, favoring plain `assert` statements and powerful fixtures.

### Parameterized Tests (`@pytest.mark.parametrize`)
Cover multiple boundary cases cleanly without duplicating test functions:
```python
import pytest
from app.calculator import calculate_discount

@pytest.mark.parametrize(
    "subtotal, customer_tier, expected_discount",
    [
        (100.0, "standard", 0.0),    # Baseline / happy path
        (100.0, "vip", 15.0),         # Business tier rule
        (0.0, "vip", 0.0),            # Boundary: zero subtotal
        (50.0, "unknown", 0.0),       # Edge: unmapped tier fallback
    ],
)
def test_calculate_discount_boundaries(subtotal, customer_tier, expected_discount):
    assert calculate_discount(subtotal, customer_tier) == pytest.approx(expected_discount)
```

### Mocking Time & External I/O
Use `monkeypatch` or `pytest-mock` (`mocker`) rather than raw `unittest.mock.patch` decorators:
```python
def test_order_submission_calls_gateway(mocker):
    mock_post = mocker.patch("app.gateway.requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"transaction_id": "tx_123"}

    order = submit_order(order_id="ord_456")

    assert order.status == "CONFIRMED"
    mock_post.assert_called_once()
```

---

## 2. JavaScript / TypeScript (`Vitest` / `Jest`)

Modern JS/TS relies heavily on Vitest or Jest with `describe`, `it`/`test`, and `expect`.

### Parameterized Tests (`test.each`)
```typescript
import { describe, it, expect } from "vitest";
import { parseUserRole } from "./role-parser";

describe("parseUserRole", () => {
  it.each([
    ["admin", "ADMIN"],
    ["editor", "EDITOR"],
    ["GUEST", "GUEST"],
    ["", "ANONYMOUS"],       // Edge: empty string
    [null, "ANONYMOUS"],     // Boundary: null input
  ])("given '%s', returns parsed role '%s'", (input, expected) => {
    expect(parseUserRole(input)).toBe(expected);
  });
});
```

### Deterministic Async & Fake Timers
Prevent flaky timeout tests by replacing real wall-clock delays with fake timers:
```typescript
import { vi, describe, it, expect, beforeEach, afterEach } from "vitest";
import { DebouncedSearch } from "./search";

describe("DebouncedSearch", () => {
  beforeEach(() => { vi.useFakeTimers(); });
  afterEach(() => { vi.useRealTimers(); });

  it("triggers query only after 300ms debounce interval", () => {
    const callback = vi.fn();
    const search = new DebouncedSearch(callback);

    search.type("query");
    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(300);
    expect(callback).toHaveBeenCalledOnce();
  });
});
```

---

## 3. Go (`testing` Package)

Go's idiomatic standard is **table-driven tests** using standard structs and subtests with `t.Run`.

### Table-Driven Subtests
```go
package invoice_test

import (
	"testing"
	"app/invoice"
)

func TestCalculateTax(t *testing.T) {
	tests := []struct {
		name       string
		amount     float64
		state      string
		expectedTax float64
		wantErr    bool
	}{
		{name: "standard taxable state", amount: 100.0, state: "NY", expectedTax: 8.875, wantErr: false},
		{name: "zero tax state", amount: 100.0, state: "DE", expectedTax: 0.0, wantErr: false},
		{name: "zero amount", amount: 0.0, state: "NY", expectedTax: 0.0, wantErr: false},
		{name: "invalid negative amount", amount: -10.0, state: "NY", expectedTax: 0.0, wantErr: true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := invoice.CalculateTax(tt.amount, tt.state)
			if (err != nil) != tt.wantErr {
				t.Fatalf("CalculateTax() error = %v, wantErr %v", err, tt.wantErr)
			}
			if got != tt.expectedTax {
				t.Errorf("CalculateTax() = %v, want %v", got, tt.expectedTax)
			}
		})
	}
}
```

---

## 4. Java (`JUnit 5` & `AssertJ`)

JUnit 5 provides rich parameterization and assertion chaining.

### Parameterized Tests (`@ParameterizedTest`)
```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.assertj.core.api.Assertions.assertThat;

class PasswordValidatorTest {

    @ParameterizedTest(name = "password ''{0}'' validity should be {1}")
    @CsvSource({
        "ValidP@ssw0rd, true",
        "short, false",             // Edge: under minimum length
        "'', false",                 // Boundary: empty string
        "alllowercasepassword, false"// Missing uppercase & digits
    })
    void validatePasswordCriteria(String candidate, boolean expectedValid) {
        PasswordValidator validator = new PasswordValidator();
        assertThat(validator.isValid(candidate)).isEqualTo(expectedValid);
    }
}
```

---

## 5. Rust (`cargo test`)

Rust integrates tests natively into the toolchain, distinguishing inline unit tests from `/tests` integration suites.

### Inline Unit Testing with Result Return
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_valid_ip_returns_address() -> Result<(), Box<dyn std::error::Error>> {
        let addr = parse_address("127.0.0.1:8080")?;
        assert_eq!(addr.port(), 8080);
        Ok(())
    }

    #[test]
    #[should_panic(expected = "Empty input")]
    fn parse_empty_ip_panics() {
        parse_address("").unwrap();
    }
}
```

---

## 6. PHP & Laravel (`Pest PHP` & `PHPUnit`)

Modern PHP and Laravel rely on **Pest PHP** (an expressive testing framework built on top of PHPUnit) or standard **PHPUnit**.

### Pest PHP with Datasets (`with()`)
Pest provides clean, readable parameterization via datasets:
```php
<?php

use App\Services\TaxCalculator;

it('calculates tax correctly across rate tiers', function (float $amount, string $country, float $expectedTax) {
    $calculator = new TaxCalculator();

    expect($calculator->calculate($amount, $country))->toBe($expectedTax);
})->with([
    'standard EU rate' => [100.0, 'FR', 20.0],
    'reduced rate'     => [100.0, 'DE', 19.0],
    'zero tax rate'    => [100.0, 'US', 0.0],
    'zero amount'      => [0.0,   'FR', 0.0],
]);
```

### Laravel Feature & HTTP Testing
Laravel makes testing HTTP endpoints, authentication, and database transactions idiomatic:
```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class InvoiceApiTest extends TestCase
{
    use RefreshDatabase; // Automatically rolls back database migrations/transactions after each test

    public function test_authenticated_user_can_create_invoice(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->postJson('/api/invoices', [
            'amount' => 1500,
            'client_email' => 'client@example.com',
        ]);

        $response->assertStatus(201)
                 ->assertJsonPath('data.amount', 1500)
                 ->assertJsonStructure(['data' => ['id', 'amount', 'created_at']]);

        $this->assertDatabaseHas('invoices', [
            'user_id' => $user->id,
            'amount'  => 1500,
        ]);
    }

    public function test_rejects_negative_invoice_amount(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->postJson('/api/invoices', [
            'amount' => -100,
            'client_email' => 'client@example.com',
        ]);

        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['amount']);
    }
}
```

### Laravel Facade Fakes (Stateful Test Doubles)
Laravel provides native, high-confidence fakes for queues, events, HTTP, and mail without brittle third-party mocking:
```php
<?php

use App\Events\OrderPlaced;
use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Mail;

public function test_checkout_dispatches_events_and_emails(): void
{
    Event::fake([OrderPlaced::class]);
    Mail::fake();
    Http::fake([
        'api.stripe.com/*' => Http::response(['id' => 'ch_123', 'status' => 'succeeded'], 200),
    ]);

    // Perform checkout action...

    Event::assertDispatched(OrderPlaced::class);
    Mail::assertSent(OrderShipped::class);
    Http::assertSent(fn ($request) => str_contains($request->url(), 'api.stripe.com'));
}
```

---

## 7. Summary Comparison Table

| Language / Tool | Parameterized Syntax | Mocking Mechanism | Async & Isolation Handling |
|---|---|---|---|
| **Python (`pytest`)** | `@pytest.mark.parametrize` | `pytest-mock` (`mocker`) / `monkeypatch` | `pytest-asyncio` |
| **JS/TS (`Vitest`)** | `it.each([ ... ])` | `vi.fn()`, `vi.spyOn()` | `async / await`, `vi.useFakeTimers()` |
| **Go (`testing`)** | `[]struct` + `t.Run()` | Interface fakes / `testify/mock` | `sync.WaitGroup`, channels |
| **Java (`JUnit 5`)** | `@ParameterizedTest` + `@CsvSource` | `Mockito` (`@Mock`, `@Spy`) | `CompletableFuture.join()` |
| **Rust (`cargo test`)** | Manual loop or `rstest` crate | Trait mocks (`mockall`) | `#[tokio::test]` |
| **PHP / Laravel (`Pest` / `PHPUnit`)** | `->with([...])` (Pest) / `@dataProvider` | `Event::fake()`, `Http::fake()`, `Mockery` | `RefreshDatabase`, `Queue::fake()` |

