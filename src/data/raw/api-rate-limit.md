# Limit zapytań API (rate limit)

**Kategoria:** technical  
**Tagi:** API, rate limit, 429, integracja

## Opis problemu
Integracja klienta przestaje działać, a w logach pojawia się błąd 429 (Too Many Requests).

## Rozwiązanie
1. Każdy plan ma określony limit zapytań na minutę i na dobę.
2. Po przekroczeniu limitu API zwraca kod 429 oraz nagłówek `Retry-After`.
3. Zalecane jest wdrożenie exponential backoff po stronie klienta.
4. Aktualne limity i zużycie widać w panelu: Ustawienia → API → Użycie.
5. Tymczasowe podniesienie limitu jest możliwe po kontakcie z supportem (dla planów Pro i wyżej).

## Dodatkowe informacje
Błąd 429 nie oznacza awarii po naszej stronie. To mechanizm ochronny. Warto sprawdzić, czy klient nie uruchomił przypadkiem pętli lub zbyt częstego pollingu.
