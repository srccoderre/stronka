"""Investment endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import NotFoundError, AuthorizationError
from app.schemas.finance import InvestmentCreate, InvestmentUpdate, InvestmentResponse, InvestmentSummary
from app.schemas.base import MessageResponse
from app.services.finance import finance_service
from app.api.v1.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[InvestmentResponse])
async def get_investments(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List:
    """
    Get all investments for current user.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of investments
    """
    investments = await finance_service.get_investments(db, current_user.id)
    return investments


@router.post("", response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
async def create_investment(
    investment_create: InvestmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> InvestmentResponse:
    """
    Create a new investment.
    
    Args:
        investment_create: Investment creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created investment
    """
    investment = await finance_service.create_investment(db, current_user.id, investment_create)
    return investment


@router.get("/summary", response_model=List[InvestmentSummary])
async def get_investment_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[InvestmentSummary]:
    """
    Get investment summary by type.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Investment summary
    """
    summary = await finance_service.get_investment_summary(db, current_user.id)
    return summary


@router.get("/{investment_id}", response_model=InvestmentResponse)
async def get_investment(
    investment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> InvestmentResponse:
    """
    Get a specific investment.
    
    Args:
        investment_id: Investment ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Investment
    """
    try:
        investment = await finance_service.get_investment(db, investment_id, current_user.id)
        return investment
    except (NotFoundError, AuthorizationError) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, NotFoundError) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))


@router.patch("/{investment_id}", response_model=InvestmentResponse)
async def update_investment(
    investment_id: int,
    investment_update: InvestmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> InvestmentResponse:
    """
    Update an investment.
    
    Args:
        investment_id: Investment ID
        investment_update: Investment update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated investment
    """
    try:
        investment = await finance_service.update_investment(db, investment_id, current_user.id, investment_update)
        return investment
    except (NotFoundError, AuthorizationError) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, NotFoundError) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))


@router.delete("/{investment_id}", response_model=MessageResponse)
async def delete_investment(
    investment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Delete an investment.
    
    Args:
        investment_id: Investment ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
    """
    try:
        await finance_service.delete_investment(db, investment_id, current_user.id)
        return MessageResponse(message="Investment deleted successfully")
    except (NotFoundError, AuthorizationError) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, NotFoundError) else status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=str(e))
