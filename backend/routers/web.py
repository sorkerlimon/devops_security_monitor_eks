"""
Web monitoring API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, WebReport
from schemas import (
    WebReport as WebReportSchema,
    WebReportCreate,
    WebReportUpdate,
    MessageResponse,
    PaginatedResponse
)
from auth import get_current_active_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/web", tags=["web-monitoring"])

@router.post("/", response_model=WebReportSchema, status_code=status.HTTP_201_CREATED)
def create_web_report(
    report: WebReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new web activity report"""
    db_report = WebReport(
        user_id=current_user.id,
        **report.dict()
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report

@router.get("/", response_model=PaginatedResponse)
def get_web_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[int] = None,
    domain: Optional[str] = None,
    category: Optional[str] = None,
    is_blocked: Optional[bool] = None,
    is_whitelisted: Optional[bool] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get web activity reports with filtering and pagination"""
    query = db.query(WebReport)
    
    # Filter by user (non-admin users can only see their own reports)
    if not current_user.is_admin:
        query = query.filter(WebReport.user_id == current_user.id)
    elif user_id:
        query = query.filter(WebReport.user_id == user_id)
    
    # Apply filters
    if domain:
        query = query.filter(WebReport.domain.ilike(f"%{domain}%"))
    
    if category:
        query = query.filter(WebReport.category == category)
    
    if is_blocked is not None:
        query = query.filter(WebReport.is_blocked == is_blocked)
    
    if is_whitelisted is not None:
        query = query.filter(WebReport.is_whitelisted == is_whitelisted)
    
    if start_date:
        query = query.filter(WebReport.created_at >= start_date)
    
    if end_date:
        query = query.filter(WebReport.created_at <= end_date)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    reports = query.order_by(WebReport.created_at.desc()).offset(skip).limit(limit).all()
    
    # Calculate pages
    pages = (total + limit - 1) // limit
    
    return PaginatedResponse(
        items=[WebReportSchema.from_orm(report) for report in reports],
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=pages
    )

@router.get("/{report_id}", response_model=WebReportSchema)
def get_web_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific web report by ID"""
    query = db.query(WebReport).filter(WebReport.id == report_id)
    
    # Non-admin users can only see their own reports
    if not current_user.is_admin:
        query = query.filter(WebReport.user_id == current_user.id)
    
    report = query.first()
    if not report:
        raise HTTPException(status_code=404, detail="Web report not found")
    
    return report

@router.put("/{report_id}", response_model=WebReportSchema)
def update_web_report(
    report_id: int,
    report_update: WebReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update web report"""
    query = db.query(WebReport).filter(WebReport.id == report_id)
    
    # Non-admin users can only update their own reports
    if not current_user.is_admin:
        query = query.filter(WebReport.user_id == current_user.id)
    
    report = query.first()
    if not report:
        raise HTTPException(status_code=404, detail="Web report not found")
    
    # Update fields
    update_data = report_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(report, field, value)
    
    db.commit()
    db.refresh(report)
    
    return report

@router.delete("/{report_id}", response_model=MessageResponse)
def delete_web_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete web report"""
    query = db.query(WebReport).filter(WebReport.id == report_id)
    
    # Non-admin users can only delete their own reports
    if not current_user.is_admin:
        query = query.filter(WebReport.user_id == current_user.id)
    
    report = query.first()
    if not report:
        raise HTTPException(status_code=404, detail="Web report not found")
    
    db.delete(report)
    db.commit()
    
    return MessageResponse(message="Web report deleted successfully")

@router.get("/stats/summary")
def get_web_stats(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get web activity statistics"""
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(WebReport).filter(WebReport.created_at >= start_date)
    
    # Non-admin users can only see their own stats
    if not current_user.is_admin:
        query = query.filter(WebReport.user_id == current_user.id)
    
    total_visits = query.count()
    blocked_visits = query.filter(WebReport.is_blocked == True).count()
    suspicious_visits = query.filter(WebReport.suspicious_score >= 5).count()
    whitelisted_visits = query.filter(WebReport.is_whitelisted == True).count()
    
    # Get top domains
    domain_counts = {}
    for report in query.all():
        domain = report.domain
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    
    top_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Get category breakdown
    category_counts = {}
    for report in query.all():
        category = report.category or 'unknown'
        category_counts[category] = category_counts.get(category, 0) + 1
    
    return {
        "total_visits": total_visits,
        "blocked_visits": blocked_visits,
        "suspicious_visits": suspicious_visits,
        "whitelisted_visits": whitelisted_visits,
        "block_rate": (blocked_visits / total_visits * 100) if total_visits > 0 else 0,
        "suspicious_rate": (suspicious_visits / total_visits * 100) if total_visits > 0 else 0,
        "top_domains": top_domains,
        "category_breakdown": category_counts,
        "period_days": days
    }

@router.get("/recent/activity")
def get_recent_web_activity(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get recent web activity"""
    query = db.query(WebReport)
    
    # Non-admin users can only see their own activity
    if not current_user.is_admin:
        query = query.filter(WebReport.user_id == current_user.id)
    
    recent_reports = query.order_by(WebReport.created_at.desc()).limit(limit).all()
    
    return [WebReportSchema.from_orm(report) for report in recent_reports]

@router.post("/block-domain", response_model=MessageResponse)
def block_domain(
    domain: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Block a domain (add to blacklist)"""
    # Update all existing reports for this domain
    db.query(WebReport).filter(WebReport.domain == domain).update({
        "is_blocked": True,
        "category": "blocked"
    })
    
    db.commit()
    
    return MessageResponse(message=f"Domain {domain} blocked successfully")

@router.post("/whitelist-domain", response_model=MessageResponse)
def whitelist_domain(
    domain: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Whitelist a domain (add to whitelist)"""
    # Update all existing reports for this domain
    db.query(WebReport).filter(WebReport.domain == domain).update({
        "is_whitelisted": True,
        "is_blocked": False,
        "category": "allowed"
    })
    
    db.commit()
    
    return MessageResponse(message=f"Domain {domain} whitelisted successfully")

@router.get("/domains/top")
def get_top_domains(
    limit: int = Query(20, ge=1, le=100),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get top visited domains"""
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(WebReport).filter(WebReport.created_at >= start_date)
    
    # Non-admin users can only see their own data
    if not current_user.is_admin:
        query = query.filter(WebReport.user_id == current_user.id)
    
    # Count visits per domain
    domain_counts = {}
    for report in query.all():
        domain = report.domain
        if domain not in domain_counts:
            domain_counts[domain] = {
                "domain": domain,
                "visits": 0,
                "blocked": 0,
                "suspicious": 0,
                "last_visit": report.created_at
            }
        
        domain_counts[domain]["visits"] += 1
        if report.is_blocked:
            domain_counts[domain]["blocked"] += 1
        if report.suspicious_score >= 5:
            domain_counts[domain]["suspicious"] += 1
        if report.created_at > domain_counts[domain]["last_visit"]:
            domain_counts[domain]["last_visit"] = report.created_at
    
    # Sort by visit count and return top domains
    top_domains = sorted(domain_counts.values(), key=lambda x: x["visits"], reverse=True)[:limit]
    
    return top_domains
