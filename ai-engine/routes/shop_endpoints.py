"""
Endpoints de Compra de Robots y Avatares - FastAPI
Rutas para marketplace de robots y creación/personalización de avatares
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Añadir paths para imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from robot_marketplace.robot_marketplace import (
    robot_marketplace,
    RobotTier,
    RobotModel,
    RobotSpecialization
)
from avatar_system.avatar_customization import (
    avatar_creator,
    Gender,
    AvatarRace,
    AvatarClass,
    Accessory
)
from robot_rental_system.robot_rental import (
    rental_manager,
    AssistantType,
    RentalPeriod
)

router = APIRouter(prefix="/api/shop", tags=["shop"])


# === MODELOS PYDANTIC ===

class RobotPurchaseRequest(BaseModel):
    player_id: str
    robot_id: str

class RobotCustomizeRequest(BaseModel):
    player_id: str
    robot_id: str
    custom_name: Optional[str] = None
    color_primary: Optional[str] = None
    color_secondary: Optional[str] = None
    skin_texture: Optional[str] = None

class AvatarCreationRequest(BaseModel):
    player_id: str
    display_name: str
    gender: str
    race: str
    avatar_class: str

class AvatarCustomizeRequest(BaseModel):
    avatar_id: str
    head: Optional[str] = None
    torso: Optional[str] = None
    arms: Optional[str] = None
    legs: Optional[str] = None
    hands: Optional[str] = None
    feet: Optional[str] = None
    eye_color: Optional[str] = None
    hair_style: Optional[str] = None
    hair_color: Optional[str] = None
    skin_tone: Optional[str] = None
    facial_hair: Optional[str] = None
    body_build: Optional[str] = None

class AvatarAccessoryRequest(BaseModel):
    avatar_id: str
    accessory: str

class AvatarCosmeticRequest(BaseModel):
    avatar_id: str
    cosmetic_name: str

class RobotAssistantCreateRequest(BaseModel):
    owner_id: str
    assistant_type: str
    name: Optional[str] = None

class RobotAssistantRentRequest(BaseModel):
    bot_id: str
    renter_id: str
    period: str


# === RUTAS DE MARKETPLACE DE ROBOTS ===

@router.get("/robots/available")
async def get_available_robots(
    tier: Optional[str] = None,
    model: Optional[str] = None,
    specialization: Optional[str] = None,
    max_price: Optional[float] = None
):
    """
    Obtiene robots disponibles con filtros opcionales
    Query params:
    - tier: starter, advanced, professional, legendary
    - model: defender, speedster, tank, sniper, paladin, shadow, titan, phoenix, cyborg, android
    - specialization: combat, speed, defense, balance, intelligence, strength
    - max_price: Precio máximo en ROBOT tokens
    """
    try:
        tier_enum = None
        if tier:
            try:
                tier_enum = RobotTier[tier.upper()]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Tier inválido: {tier}")
        
        model_enum = None
        if model:
            try:
                model_enum = RobotModel[model.upper()]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Modelo inválido: {model}")
        
        specialization_enum = None
        if specialization:
            try:
                specialization_enum = RobotSpecialization[specialization.upper()]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Especialización inválida: {specialization}")
        
        robots = robot_marketplace.get_available_robots(tier_enum, model_enum, specialization_enum, max_price)
        
        return {
            "success": True,
            "total": len(robots),
            "robots": [r.to_dict() for r in robots]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/robots/{robot_id}")
async def get_robot_details(robot_id: str):
    """
    Obtiene detalles de un robot específico
    """
    try:
        robot = robot_marketplace.get_robot(robot_id)
        
        if not robot:
            raise HTTPException(status_code=404, detail="Robot no encontrado")
        
        return {
            "success": True,
            "robot": robot.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/robots/purchase")
async def purchase_robot(request: RobotPurchaseRequest):
    """
    Compra un robot del marketplace
    Body:
    - player_id: ID del jugador
    - robot_id: ID del robot a comprar
    """
    try:
        result = robot_marketplace.purchase_robot(request.player_id, request.robot_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": result["message"],
            "robot": result["robot"],
            "price_paid": result["price"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/robots/player/{player_id}")
async def get_player_robots(player_id: str):
    """
    Obtiene robots del jugador
    """
    try:
        robots = robot_marketplace.get_player_robots(player_id)
        
        return {
            "success": True,
            "player_id": player_id,
            "total": len(robots),
            "robots": [r.to_dict() for r in robots]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/robots/customize")
async def customize_robot(request: RobotCustomizeRequest):
    """
    Personaliza un robot del jugador
    Body:
    - player_id: ID del jugador
    - robot_id: ID del robot
    - custom_name: Nombre personalizado (opcional)
    - color_primary: Color primario (opcional)
    - color_secondary: Color secundario (opcional)
    - skin_texture: Textura de piel (opcional)
    """
    try:
        result = robot_marketplace.customize_robot(
            request.player_id,
            request.robot_id,
            request.custom_name or "",
            request.color_primary or "",
            request.color_secondary or "",
            request.skin_texture or ""
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": "Robot personalizado",
            "customization": result["customization"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === RUTAS DE AVATARES ===

@router.post("/avatars/create")
async def create_avatar(request: AvatarCreationRequest):
    """
    Crea nuevo avatar
    Body:
    - player_id: ID del jugador
    - display_name: Nombre del avatar
    - gender: male, female, non_binary, android
    - race: human, cyborg, android, alien, hologram, hybrid
    - avatar_class: warrior, mage, rogue, paladin, ranger, scientist, hacker, entrepreneur
    """
    try:
        try:
            gender_enum = Gender[request.gender.upper()]
            race_enum = AvatarRace[request.race.upper()]
            class_enum = AvatarClass[request.avatar_class.upper()]
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Valor inválido: {str(e)}")
        
        avatar = avatar_creator.create_avatar(
            request.player_id,
            request.display_name,
            gender_enum,
            race_enum,
            class_enum
        )
        
        return {
            "success": True,
            "message": "Avatar creado exitosamente",
            "avatar": avatar.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/avatars/{avatar_id}")
async def get_avatar_details(avatar_id: str):
    """
    Obtiene detalles del avatar
    """
    try:
        avatar = avatar_creator.get_avatar(avatar_id)
        
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar no encontrado")
        
        return {
            "success": True,
            "avatar": avatar.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/avatars/player/{player_id}")
async def get_player_avatars(player_id: str):
    """
    Obtiene avatares del jugador
    """
    try:
        avatars = avatar_creator.get_player_avatars(player_id)
        
        return {
            "success": True,
            "player_id": player_id,
            "total": len(avatars),
            "avatars": [a.to_dict() for a in avatars]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/avatars/customize")
async def customize_avatar(request: AvatarCustomizeRequest):
    """
    Personaliza apariencia del avatar
    Body: Partes del cuerpo a customizar (opcionales)
    """
    try:
        customization = {}
        for field, value in request.dict().items():
            if field != "avatar_id" and value is not None:
                customization[field] = value
        
        result = avatar_creator.customize_avatar(request.avatar_id, **customization)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": "Avatar personalizado",
            "appearance": result["appearance"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/avatars/accessory")
async def add_avatar_accessory(request: AvatarAccessoryRequest):
    """
    Añade accesorio a avatar
    Body:
    - avatar_id: ID del avatar
    - accessory: helmet, glasses, hat, cape, wings, aura, crown, halo, mask, earrings
    """
    try:
        try:
            accessory_enum = Accessory[request.accessory.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Accesorio inválido: {request.accessory}")
        
        result = avatar_creator.add_avatar_accessory(request.avatar_id, accessory_enum)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": "Accesorio añadido",
            "accessory": result["accessory"],
            "total_accessories": result["total_accessories"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/avatars/cosmetic/purchase")
async def purchase_cosmetic(request: AvatarCosmeticRequest):
    """
    Compra cosmético para avatar
    Body:
    - avatar_id: ID del avatar
    - cosmetic_name: Nombre del cosmético
    """
    try:
        result = avatar_creator.purchase_cosmetic(request.avatar_id, request.cosmetic_name)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": "Cosmético comprado",
            "cosmetic": result["cosmetic"],
            "price": result["price"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cosmetics/shop")
async def get_cosmetic_shop():
    """
    Obtiene tienda de cosméticos disponibles
    """
    try:
        shop = avatar_creator.get_cosmetic_shop()
        
        return {
            "success": True,
            "shop": shop
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === RUTAS DE ROBOTS ASISTENTES ===

@router.post("/assistants/create")
async def create_assistant(request: RobotAssistantCreateRequest):
    """
    Crea robot asistente rentable
    Body:
    - owner_id: ID del propietario
    - assistant_type: personal, corporate, medical, research, security, logistics, entertainment, education
    - name: Nombre personalizado (opcional)
    """
    try:
        try:
            assistant_type_enum = AssistantType[request.assistant_type.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Tipo de asistente inválido: {request.assistant_type}")
        
        bot = rental_manager.create_bot(request.owner_id, assistant_type_enum, request.name)
        
        return {
            "success": True,
            "message": "Robot asistente creado",
            "bot": bot.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assistants/marketplace")
async def get_rental_marketplace():
    """
    Obtiene marketplace de robots para rentar
    """
    try:
        marketplace = rental_manager.get_rental_marketplace()
        
        return {
            "success": True,
            "total_available": len(marketplace),
            "bots": marketplace
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/assistants/rent")
async def rent_assistant(request: RobotAssistantRentRequest):
    """
    Renta robot asistente
    Body:
    - bot_id: ID del bot
    - renter_id: ID del que renta
    - period: hourly, daily, weekly, monthly
    """
    try:
        try:
            period_enum = RentalPeriod[request.period.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Período inválido: {request.period}")
        
        result = rental_manager.rent_bot(request.bot_id, request.renter_id, period_enum)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": "Bot rentado exitosamente",
            "rental": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === ESTADÍSTICAS ===

@router.get("/stats/marketplace")
async def get_marketplace_stats():
    """
    Obtiene estadísticas del marketplace de robots
    """
    try:
        stats = robot_marketplace.get_marketplace_stats()
        
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/avatars")
async def get_avatar_stats():
    """
    Obtiene estadísticas globales de avatares
    """
    try:
        stats = avatar_creator.get_global_stats()
        
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
