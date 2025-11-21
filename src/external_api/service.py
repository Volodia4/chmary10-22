# src/external_api/services.py
import requests
from src.external_api.models import CatFactModel, CatImageModel, CatCombinedModel
from src.cache.service import cache_get, cache_set
from src.settings import settings


class CatService:
    fact_url: str = "https://catfact.ninja/fact"
    image_url: str = "https://api.thecatapi.com/v1/images/search"

    async def get_cat_fact(self) -> CatFactModel:
        cache_key = "cache:external:cat_fact"

        # Асинхронно отримуємо з кешу
        cached = await cache_get(cache_key)
        if cached:
            print("✅ Cache HIT for cat_fact")
            return CatFactModel(**cached)

        print("❌ Cache MISS for cat_fact")

        # Фетчимо з API
        response = requests.get(self.fact_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Асинхронно зберігаємо в кеш
        await cache_set(cache_key, data, settings.redis_TTL)
        print("💾 Saved to cache: cat_fact")

        return CatFactModel(**data)

    async def get_cat_image(self) -> CatImageModel:
        cache_key = "cache:external:cat_image"

        # Асинхронно отримуємо з кешу
        cached = await cache_get(cache_key)
        if cached:
            print("✅ Cache HIT for cat_image")
            return CatImageModel(url=cached["url"])

        print("❌ Cache MISS for cat_image")

        # Фетчимо з API
        response = requests.get(self.image_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Асинхронно зберігаємо в кеш
        await cache_set(cache_key, {"url": data[0]["url"]}, settings.redis_TTL)
        print("💾 Saved to cache: cat_image")

        return CatImageModel(url=data[0]["url"])

    async def get_cat_info(self) -> CatCombinedModel:
        fact = await self.get_cat_fact()
        image = await self.get_cat_image()
        return CatCombinedModel(fact=fact.fact, image_url=image.url)


service = CatService()
