# Webhooki nie dochodzą do systemu klienta

**Kategoria:** technical  
**Tagi:** webhook, integracja, endpoint, błąd dostawy

## Opis problemu
Skonfigurowane webhooki nie są dostarczane lub wracają z błędem 4xx/5xx.

## Rozwiązanie
1. Sprawdź w panelu: Integracje → Webhooki → Historia dostaw.
2. Upewnij się, że endpoint klienta odpowiada kodem 2xx w czasie max 5 sekund.
3. Zweryfikuj poprawność URL (https) oraz ewentualny sekret podpisu.
4. Można ponowić ostatnie nieudane dostawy ręcznie z panelu.
5. Po 10 nieudanych próbach webhook jest automatycznie wyłączany – trzeba go włączyć ponownie.

## Dodatkowe informacje
W logach widać dokładny kod odpowiedzi i treść błędu zwróconą przez serwer klienta. To zwykle najszybsza droga do diagnozy.
