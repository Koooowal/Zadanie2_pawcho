# Zadanie 2 – GitHub Actions + Docker + CVE Scan

Repozytorium zawiera pipeline GitHub Actions do:
- Budowania obrazu kontenera dla architektur `linux/amd64` i `linux/arm64`
- Użycia cache dla Buildx w DockerHub
- Skanowania obrazu przy użyciu Trivy pod kątem CVE
- Publikowania obrazu do GitHub Container Registry (ghcr.io) tylko jeśli nie wykryto błędów krytycznych i wysokich

## Wymagania

- Utworzenie `DOCKERHUB_USERNAME` i `DOCKERHUB_TOKEN` w sekcjach secrets w repozytorium
- Publiczny repozytorium obrazu na DockerHub: `yourdockerhubusername/cache-repo`

## Tagowanie

- `latest`: najnowsza wersja
- `GITHUB_SHA`: unikalna wersja commitowa
- `cache`: tag wykorzystywany do przechowywania danych build-cache

## Uruchomienie

Pipeline uruchamia się automatycznie przy każdym pushu do gałęzi `main`.

## Źródła

- [Trivy](https://github.com/aquasecurity/trivy)
- [GitHub Actions: docker/build-push-action](https://github.com/docker/build-push-action)
- [BuildKit Registry Cache](https://docs.docker.com/build/cache/backends/registry/)
