# Zadanie 2 – GitHub Actions: Budowa obrazu, cache, CVE Scan i publikacja

## Cel

Celem zadania było opracowanie automatycznego łańcucha (pipeline) w usłudze **GitHub Actions**, który:

1. Buduje obraz kontenera na podstawie `Dockerfile` oraz kodów źródłowych aplikacji.
2. Wspiera architektury `linux/amd64` oraz `linux/arm64`.
3. Wykorzystuje cache BuildKit (eksporter i backend typu `registry`, tryb `max`) przechowywany w **dedykowanym publicznym repozytorium na DockerHub**.
4. Wykonuje test podatności CVE (Trivy) i publikuje obraz do `ghcr.io` tylko wtedy, gdy nie występują zagrożenia krytyczne ani wysokie.

---

## Struktura rozwiązania

Pipeline został zdefiniowany w pliku:

```
.github/workflows/docker-build.yml
```

---

## Szczegóły implementacji

### ✅ Budowa wieloarchitekturowa

Do budowy obrazu wykorzystano `docker/build-push-action` z platformami:

```yaml
platforms: linux/amd64,linux/arm64
```

Umożliwia to utworzenie jednego manifestu wspierającego obie architektury.

---

### ✅ Cache Buildx z DockerHub

Wykorzystano:

```yaml
cache-to: type=registry,ref=docker.io/<nazwa_użytkownika>/cache-repo:cache,mode=max
cache-from: type=registry,ref=docker.io/<nazwa_użytkownika>/cache-repo:cache
```

* `type=registry` pozwala przechowywać cache jako warstwy obrazu w repozytorium DockerHub.
* `mode=max` zapewnia maksymalną skuteczność (pełna de-duplikacja warstw builda).

Dzięki temu czas budowania skraca się znacznie przy kolejnych uruchomieniach workflow.

---

### ✅ Skanowanie obrazu: Trivy

Zastosowano skaner **Trivy** (Aquasecurity) jako etap bezpieczeństwa przed publikacją. Komenda uruchamiana w pipeline:

```bash
trivy image --exit-code 1 --severity CRITICAL,HIGH ghcr.io/<nazwa_użytkownika>/<repo>:temp
```

* `--exit-code 1` powoduje przerwanie pipeline w razie wykrycia poważnych podatności.
* Dopiero po pozytywnym przejściu testu, obraz jest tagowany jako `latest` i pushowany do `ghcr.io`.

**Uzasadnienie wyboru Trivy:** narzędzie jest proste w integracji, open-source, posiada aktywną społeczność i wsparcie CI/CD (w tym GitHub Actions). Lepszy wybór od Docker Scout ze względu na przejrzystość i możliwość konfiguracji poziomów krytyczności.


---

### ✅ Publikacja do GitHub Container Registry (GHCR)

Po pozytywnym wyniku skanowania, obraz jest przesyłany do publicznego repozytorium:

```
ghcr.io/<nazwa_użytkownika>/<repo>:latest
ghcr.io/<nazwa_użytkownika>/<repo>:<SHA>
```

---

## Tagowanie obrazów i cache

### Obrazy:

* `latest` – ostatnia wersja z gałęzi `main`
* `${{ github.sha }}` – unikalna wersja na podstawie commita (identyfikowalność buildów)

### Cache:

* `cache` – tag dedykowany do przechowywania danych cache w repozytorium DockerHub

**Uzasadnienie:**

* `GITHUB_SHA` gwarantuje niezmienność konkretnej wersji.
* `latest` zapewnia łatwy dostęp do najnowszego działającego obrazu.
* Osobny tag `cache` izoluje dane cache od wersji produkcyjnych i jest kompatybilny z mechanizmem BuildKit Registry Cache.


---

## Wymagania środowiskowe (secrets)

W repozytorium GitHub należy skonfigurować:

* `DOCKERHUB_USERNAME` – nazwa użytkownika DockerHub
* `DOCKERHUB_TOKEN` – token dostępu (z DockerHub)
* `GHCR_PAT` – personal access token GitHub z uprawnieniem `write:packages`

---

## Uruchomienie

Pipeline uruchamia się automatycznie przy pushu do gałęzi `main`.
Przykładowe działania można podejrzeć w zakładce **Actions** repozytorium.

---

## Podsumowanie

Pipeline GitHub Actions został zrealizowany zgodnie z wytycznymi.
Spełnia wymagania wieloarchitekturowości, użycia cache, automatycznego skanowania i bezpiecznej publikacji obrazu.

---
