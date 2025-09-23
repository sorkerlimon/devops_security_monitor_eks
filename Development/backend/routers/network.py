"""
Network monitoring API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, NetworkReport
from schemas import (
    NetworkReport as NetworkReportSchema,
    NetworkReportCreate,
    NetworkReportUpdate,
    MessageResponse,
    PaginatedResponse
)
from auth import get_current_active_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/network", tags=["network-monitoring"])

@router.post("/", response_model=NetworkReportSchema, status_code=status.HTTP_201_CREATED)
def create_network_report(
    report: NetworkReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new network monitoring report"""
    db_report = NetworkReport(
        user_id=current_user.id,
        **report.dict()
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report

@router.get("/", response_model=PaginatedResponse)
def get_network_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[int] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    is_open: Optional[bool] = None,
    status_filter: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get network monitoring reports with filtering and pagination"""
    query = db.query(NetworkReport)
    
    # Filter by user (non-admin users can only see their own reports)
    if not current_user.is_admin:
        query = query.filter(NetworkReport.user_id == current_user.id)
    elif user_id:
        query = query.filter(NetworkReport.user_id == user_id)
    
    # Apply filters
    if host:
        query = query.filter(NetworkReport.host.ilike(f"%{host}%"))
    
    if port:
        query = query.filter(NetworkReport.port == port)
    
    if is_open is not None:
        query = query.filter(NetworkReport.is_open == is_open)
    
    if status_filter:
        query = query.filter(NetworkReport.status == status_filter)
    
    if start_date:
        query = query.filter(NetworkReport.created_at >= start_date)
    
    if end_date:
        query = query.filter(NetworkReport.created_at <= end_date)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    reports = query.order_by(NetworkReport.created_at.desc()).offset(skip).limit(limit).all()
    
    # Calculate pages
    pages = (total + limit - 1) // limit
    
    return PaginatedResponse(
        items=[NetworkReportSchema.from_orm(report) for report in reports],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=pages
    )

@router.get("/{report_id}", response_model=NetworkReportSchema)
def get_network_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific network report by ID"""
    query = db.query(NetworkReport).filter(NetworkReport.id == report_id)
    
    # Non-admin users can only see their own reports
    if not current_user.is_admin:
        query = query.filter(NetworkReport.user_id == current_user.id)
    
    report = query.first()
    if not report:
        raise HTTPException(status_code=404, detail="Network report not found")
    
    return report

@router.put("/{report_id}", response_model=NetworkReportSchema)
def update_network_report(
    report_id: int,
    report_update: NetworkReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update network report"""
    query = db.query(NetworkReport).filter(NetworkReport.id == report_id)
    
    # Non-admin users can only update their own reports
    if not current_user.is_admin:
        query = query.filter(NetworkReport.user_id == current_user.id)
    
    report = query.first()
    if not report:
        raise HTTPException(status_code=404, detail="Network report not found")
    
    # Update fields
    update_data = report_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(report, field, value)
    
    db.commit()
    db.refresh(report)
    
    return report

@router.delete("/{report_id}", response_model=MessageResponse)
def delete_network_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete network report"""
    query = db.query(NetworkReport).filter(NetworkReport.id == report_id)
    
    # Non-admin users can only delete their own reports
    if not current_user.is_admin:
        query = query.filter(NetworkReport.user_id == current_user.id)
    
    report = query.first()
    if not report:
        raise HTTPException(status_code=404, detail="Network report not found")
    
    db.delete(report)
    db.commit()
    
    return MessageResponse(message="Network report deleted successfully")

@router.get("/stats/summary")
def get_network_stats(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get network monitoring statistics"""
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(NetworkReport).filter(NetworkReport.created_at >= start_date)
    
    # Non-admin users can only see their own stats
    if not current_user.is_admin:
        query = query.filter(NetworkReport.user_id == current_user.id)
    
    total_scans = query.count()
    open_ports = query.filter(NetworkReport.is_open == True).count()
    closed_ports = query.filter(NetworkReport.is_open == False).count()
    
    # Get top ports
    port_counts = {}
    for report in query.all():
        port = report.port
        port_counts[port] = port_counts.get(port, 0) + 1
    
    top_ports = sorted(port_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        "total_scans": total_scans,
        "open_ports": open_ports,
        "closed_ports": closed_ports,
        "open_rate": (open_ports / total_scans * 100) if total_scans > 0 else 0,
        "top_ports": top_ports,
        "period_days": days
    }
