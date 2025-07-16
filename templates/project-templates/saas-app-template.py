#!/usr/bin/env python3
"""
SaaS App Template Generator
===========================

Creates a complete SaaS application with:
- Multi-tenant architecture
- Subscription management
- Payment integration
- User authentication
- Analytics and monitoring
- AI-powered development tools

Usage:
    python saas-app-template.py --name my-saas --framework next --database postgresql
"""

import os
import sys
import json
import yaml
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SaaSAppTemplateGenerator:
    """Generator for SaaS application templates"""
    
    def __init__(self):
        self.templates_dir = Path("/mnt/c/bmad-workspace/templates")
        self.saas_frameworks = {
            "next": {
                "language": "typescript",
                "backend": "api-routes",
                "database": ["postgresql", "mongodb", "supabase"],
                "auth": ["next-auth", "auth0", "supabase-auth"],
                "payments": ["stripe", "paddle", "lemonsqueezy"]
            },
            "nuxt": {
                "language": "typescript",
                "backend": "nuxt-server",
                "database": ["postgresql", "mongodb", "supabase"],
                "auth": ["nuxt-auth", "auth0", "supabase-auth"],
                "payments": ["stripe", "paddle", "lemonsqueezy"]
            },
            "remix": {
                "language": "typescript",
                "backend": "remix-server",
                "database": ["postgresql", "mongodb", "supabase"],
                "auth": ["remix-auth", "auth0", "supabase-auth"],
                "payments": ["stripe", "paddle", "lemonsqueezy"]
            },
            "sveltekit": {
                "language": "typescript",
                "backend": "sveltekit-server",
                "database": ["postgresql", "mongodb", "supabase"],
                "auth": ["sveltekit-auth", "auth0", "supabase-auth"],
                "payments": ["stripe", "paddle", "lemonsqueezy"]
            },
            "fastapi": {
                "language": "python",
                "backend": "fastapi",
                "database": ["postgresql", "mongodb"],
                "auth": ["fastapi-auth", "auth0"],
                "payments": ["stripe", "paddle"]
            }
        }
        
        self.saas_features = {
            "multi_tenant": "Multi-tenant architecture with tenant isolation",
            "subscription_management": "Subscription plans and billing management",
            "payment_integration": "Payment processing with webhooks",
            "user_authentication": "Secure user authentication and authorization",
            "role_based_access": "Role-based access control (RBAC)",
            "api_management": "API rate limiting and management",
            "analytics": "User analytics and business metrics",
            "monitoring": "Application monitoring and alerting",
            "admin_dashboard": "Admin dashboard for management",
            "user_onboarding": "User onboarding and tutorials",
            "email_notifications": "Email notifications and campaigns",
            "file_storage": "File upload and storage",
            "search": "Full-text search functionality",
            "webhooks": "Webhook system for integrations",
            "audit_logging": "Comprehensive audit logging"
        }
    
    def generate_saas_app(self, name: str, framework: str, options: Dict) -> str:
        """Generate a complete SaaS application"""
        logger.info(f"🚀 Generating SaaS application: {name}")
        
        # Create project directory
        project_dir = f"/mnt/c/bmad-workspace/projects/{name}"
        os.makedirs(project_dir, exist_ok=True)
        
        # Generate project structure
        self._create_saas_structure(project_dir, framework, options)
        
        # Generate core configuration
        self._generate_saas_config(project_dir, name, framework, options)
        
        # Generate authentication system
        self._generate_auth_system(project_dir, framework, options)
        
        # Generate subscription management
        self._generate_subscription_system(project_dir, framework, options)
        
        # Generate payment integration
        self._generate_payment_system(project_dir, framework, options)
        
        # Generate multi-tenant architecture
        self._generate_multi_tenant_system(project_dir, framework, options)
        
        # Generate admin dashboard
        self._generate_admin_dashboard(project_dir, framework, options)
        
        # Generate API management
        self._generate_api_management(project_dir, framework, options)
        
        # Generate analytics system
        self._generate_analytics_system(project_dir, framework, options)
        
        # Generate monitoring and logging
        self._generate_monitoring_system(project_dir, framework, options)
        
        # Generate deployment configuration
        self._generate_deployment_config(project_dir, framework, options)
        
        # Generate documentation
        self._generate_saas_documentation(project_dir, name, framework, options)
        
        # Generate AI integration
        self._generate_ai_integration(project_dir, name, framework, options)
        
        # Initialize git repository
        self._initialize_git(project_dir)
        
        logger.info(f"✅ SaaS application {name} generated successfully at {project_dir}")
        return project_dir
    
    def _create_saas_structure(self, project_dir: str, framework: str, options: Dict):
        """Create SaaS application structure"""
        
        if framework == "next":
            structure = [
                "src/app", "src/components", "src/lib", "src/hooks", "src/utils",
                "src/types", "src/store", "src/middleware", "src/auth",
                "src/payments", "src/subscriptions", "src/tenants", "src/analytics",
                "src/admin", "src/api", "src/emails", "src/webhooks",
                "public", "prisma", "supabase", "tests", "docs", "scripts",
                "config", "logs", ".github/workflows"
            ]
        elif framework == "fastapi":
            structure = [
                "src/api", "src/auth", "src/payments", "src/subscriptions",
                "src/tenants", "src/analytics", "src/admin", "src/models",
                "src/schemas", "src/services", "src/database", "src/utils",
                "src/middleware", "src/emails", "src/webhooks", "src/config",
                "tests", "docs", "scripts", "migrations", "logs", ".github/workflows"
            ]
        else:
            # Generic structure for other frameworks
            structure = [
                "src", "components", "lib", "utils", "types", "store",
                "auth", "payments", "subscriptions", "tenants", "analytics",
                "admin", "api", "emails", "webhooks", "tests", "docs",
                "scripts", "config", "logs", ".github/workflows"
            ]
        
        # Create directories
        for directory in structure:
            dir_path = os.path.join(project_dir, directory)
            os.makedirs(dir_path, exist_ok=True)
            
            # Create .gitkeep for empty directories
            if not os.listdir(dir_path):
                gitkeep_path = os.path.join(dir_path, ".gitkeep")
                with open(gitkeep_path, 'w') as f:
                    f.write("")
    
    def _generate_saas_config(self, project_dir: str, name: str, framework: str, options: Dict):
        """Generate SaaS configuration"""
        
        # Enhanced CLAUDE.md for SaaS
        claude_config = {
            "project_name": name,
            "project_type": "saas",
            "framework": framework,
            "version": "1.0.0",
            "saas_features": list(self.saas_features.keys()),
            "ai_tools": [
                "sequential_thinking",
                "perplexity",
                "context7",
                "playwright",
                "github",
                "taskmaster",
                "dart",
                "agentic_tools",
                "memory",
                "brave_search"
            ],
            "workflow_triggers": [
                {
                    "event": "subscription_created",
                    "action": "send_welcome_email"
                },
                {
                    "event": "payment_failed",
                    "action": "handle_payment_failure"
                },
                {
                    "event": "trial_expiring",
                    "action": "send_trial_reminder"
                },
                {
                    "event": "user_registered",
                    "action": "start_onboarding"
                }
            ],
            "quality_standards": {
                "min_test_coverage": 0.85,
                "max_complexity": 8,
                "security_scan": True,
                "performance_threshold": 1.5,
                "accessibility_compliance": "WCAG 2.1 AA"
            },
            "saas_architecture": {
                "multi_tenant": True,
                "tenant_isolation": "schema",
                "subscription_model": "freemium",
                "payment_provider": options.get("payment_provider", "stripe"),
                "auth_provider": options.get("auth_provider", "next-auth"),
                "database": options.get("database", "postgresql")
            },
            "business_metrics": [
                "monthly_recurring_revenue",
                "customer_acquisition_cost",
                "customer_lifetime_value",
                "churn_rate",
                "trial_conversion_rate"
            ]
        }
        
        claude_content = f"""---
{yaml.dump(claude_config, default_flow_style=False)}
---

# {name} - SaaS Application

## Overview

{name} is a modern SaaS application built with {framework} and enhanced with AI-powered development tools.

## SaaS Features

### Core Features
- **Multi-tenant Architecture**: Secure tenant isolation
- **Subscription Management**: Flexible subscription plans
- **Payment Processing**: Integrated payment handling
- **User Authentication**: Secure user management
- **Role-based Access Control**: Fine-grained permissions
- **Analytics Dashboard**: Business metrics and insights
- **Admin Panel**: Comprehensive admin tools

### AI-Powered Development
- **CEO Quality Control Agent**: Automated code quality assurance
- **Sequential Thinking**: Strategic business decision making
- **Perplexity Research**: Market intelligence and competitive analysis
- **Automated Testing**: Comprehensive test coverage
- **Performance Monitoring**: Real-time performance optimization

## Architecture

### Multi-Tenant Design
- **Tenant Isolation**: {claude_config['saas_architecture']['tenant_isolation']} level isolation
- **Scalable Database**: {claude_config['saas_architecture']['database']} with proper indexing
- **API Rate Limiting**: Per-tenant rate limiting
- **Resource Quotas**: Configurable resource limits per plan

### Subscription Model
- **Freemium**: Free tier with premium upgrades
- **Flexible Plans**: Monthly and annual billing
- **Usage-based Billing**: Metered features
- **Trial Management**: Automated trial handling

### Security
- **Authentication**: OAuth 2.0 with {claude_config['saas_architecture']['auth_provider']}
- **Authorization**: Role-based access control
- **Data Encryption**: End-to-end encryption
- **Audit Logging**: Comprehensive security logs

## Business Intelligence

### Key Metrics
- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (CLV)
- Churn Rate Analysis
- Trial Conversion Rates

### Analytics
- Real-time user activity tracking
- Feature usage analytics
- Performance monitoring
- Business reporting dashboard

## Development Workflow

### AI-Enhanced Development
1. **Strategic Planning**: Use Sequential Thinking for business decisions
2. **Market Research**: Perplexity integration for competitive analysis
3. **Quality Assurance**: CEO Quality Control Agent monitors all code
4. **Testing**: Automated testing with Playwright
5. **Deployment**: Continuous deployment with quality gates

### Development Process
1. Feature planning with business impact analysis
2. Development with AI assistance
3. Automatic quality control and testing
4. Deployment with monitoring
5. Analytics and optimization

## Getting Started

### Prerequisites
- Node.js 18+ (for {framework} projects)
- {claude_config['saas_architecture']['database']} database
- {claude_config['saas_architecture']['payment_provider']} account
- Email service (SendGrid, PostMark, etc.)

### Quick Start
1. Clone the repository
2. Install dependencies
3. Configure environment variables
4. Run database migrations
5. Start the development server
6. Access the admin panel

### Environment Configuration
```bash
# Application
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key

# Database
DATABASE_URL=postgresql://...

# Payment Provider
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
SENDGRID_API_KEY=SG...

# Analytics
MIXPANEL_TOKEN=...
```

## Business Model

### Subscription Tiers
- **Free**: Basic features for individuals
- **Pro**: Advanced features for professionals
- **Team**: Collaboration features for teams
- **Enterprise**: Custom solutions for large organizations

### Revenue Streams
- Monthly/Annual subscriptions
- Usage-based billing
- Enterprise licensing
- Professional services

## Scaling Strategy

### Technical Scaling
- Horizontal database scaling
- CDN for static assets
- Caching strategies
- Load balancing

### Business Scaling
- Customer success automation
- Sales funnel optimization
- Marketing automation
- Partner integrations

## Success Metrics

### Technical KPIs
- 99.9% uptime
- <200ms API response time
- 90%+ test coverage
- Zero security vulnerabilities

### Business KPIs
- 10% monthly growth rate
- <5% monthly churn rate
- 20%+ trial conversion rate
- $200+ average revenue per user

Your SaaS application is now ready for AI-powered development! 🚀
"""
        
        claude_path = os.path.join(project_dir, "CLAUDE.md")
        with open(claude_path, 'w') as f:
            f.write(claude_content)
    
    def _generate_auth_system(self, project_dir: str, framework: str, options: Dict):
        """Generate authentication system"""
        logger.info("Generating authentication system...")
        
        if framework == "next":
            self._generate_nextauth_config(project_dir, options)
        elif framework == "fastapi":
            self._generate_fastapi_auth(project_dir, options)
        else:
            self._generate_generic_auth(project_dir, framework, options)
    
    def _generate_nextauth_config(self, project_dir: str, options: Dict):
        """Generate NextAuth configuration"""
        
        # NextAuth configuration
        nextauth_config = """import NextAuth from 'next-auth'
import { PrismaAdapter } from '@auth/prisma-adapter'
import GoogleProvider from 'next-auth/providers/google'
import GithubProvider from 'next-auth/providers/github'
import EmailProvider from 'next-auth/providers/email'
import { prisma } from '@/lib/prisma'

export default NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    GithubProvider({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    EmailProvider({
      server: process.env.EMAIL_SERVER,
      from: process.env.EMAIL_FROM,
    }),
  ],
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  callbacks: {
    async jwt({ token, user, account }) {
      if (user) {
        token.role = user.role
        token.tenantId = user.tenantId
        token.subscriptionStatus = user.subscriptionStatus
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.sub
        session.user.role = token.role
        session.user.tenantId = token.tenantId
        session.user.subscriptionStatus = token.subscriptionStatus
      }
      return session
    },
    async signIn({ user, account, profile }) {
      // Custom sign-in logic
      const existingUser = await prisma.user.findUnique({
        where: { email: user.email },
      })
      
      if (!existingUser) {
        // Create new tenant for new user
        const tenant = await prisma.tenant.create({
          data: {
            name: user.name || 'Personal',
            slug: generateSlug(user.name || user.email),
            plan: 'free',
            trialEndsAt: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000), // 14 days
          },
        })
        
        // Update user with tenant info
        await prisma.user.update({
          where: { email: user.email },
          data: {
            tenantId: tenant.id,
            role: 'owner',
          },
        })
      }
      
      return true
    },
  },
  pages: {
    signIn: '/auth/signin',
    signUp: '/auth/signup',
    error: '/auth/error',
  },
  events: {
    async signIn({ user, account, profile, isNewUser }) {
      if (isNewUser) {
        // Send welcome email
        await sendWelcomeEmail(user.email, user.name)
        
        // Track user registration
        await trackEvent('user_registered', {
          userId: user.id,
          provider: account.provider,
        })
      }
    },
  },
})

function generateSlug(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .substring(0, 50)
}
"""
        
        nextauth_path = os.path.join(project_dir, "src/auth/auth.ts")
        with open(nextauth_path, 'w') as f:
            f.write(nextauth_config)
        
        # Auth utilities
        auth_utils = """import { getServerSession } from 'next-auth'
import { authOptions } from './auth'
import { prisma } from '@/lib/prisma'

export async function getCurrentUser() {
  const session = await getServerSession(authOptions)
  return session?.user
}

export async function requireAuth() {
  const user = await getCurrentUser()
  if (!user) {
    throw new Error('Authentication required')
  }
  return user
}

export async function requireRole(requiredRole: string) {
  const user = await requireAuth()
  if (user.role !== requiredRole) {
    throw new Error('Insufficient permissions')
  }
  return user
}

export async function requireSubscription() {
  const user = await requireAuth()
  if (user.subscriptionStatus !== 'active') {
    throw new Error('Active subscription required')
  }
  return user
}

export async function getTenantWithPermissions(tenantId: string, userId: string) {
  const tenant = await prisma.tenant.findFirst({
    where: {
      id: tenantId,
      users: {
        some: {
          id: userId,
        },
      },
    },
    include: {
      users: true,
      subscription: true,
    },
  })
  
  if (!tenant) {
    throw new Error('Tenant not found or access denied')
  }
  
  return tenant
}
"""
        
        auth_utils_path = os.path.join(project_dir, "src/auth/utils.ts")
        with open(auth_utils_path, 'w') as f:
            f.write(auth_utils)
        
        # Auth middleware
        auth_middleware = """import { withAuth } from 'next-auth/middleware'

export default withAuth(
  function middleware(req) {
    // Additional middleware logic
    const { pathname } = req.nextUrl
    const token = req.nextauth.token
    
    // Admin routes
    if (pathname.startsWith('/admin') && token?.role !== 'admin') {
      return Response.redirect(new URL('/dashboard', req.url))
    }
    
    // Subscription required routes
    if (pathname.startsWith('/pro') && token?.subscriptionStatus !== 'active') {
      return Response.redirect(new URL('/pricing', req.url))
    }
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token,
    },
  }
)

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*', '/pro/:path*', '/api/protected/:path*'],
}
"""
        
        middleware_path = os.path.join(project_dir, "src/middleware.ts")
        with open(middleware_path, 'w') as f:
            f.write(auth_middleware)
    
    def _generate_fastapi_auth(self, project_dir: str, options: Dict):
        """Generate FastAPI authentication system"""
        
        # FastAPI auth dependencies
        auth_deps = """from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from .models import User, Tenant
from .database import get_db
from .config import settings

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise AuthenticationError()
    except JWTError:
        raise AuthenticationError()
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise AuthenticationError()
    return user

async def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise AuthorizationError()
        return current_user
    return role_checker

async def require_active_subscription(current_user: User = Depends(get_current_user)):
    if current_user.subscription_status != 'active':
        raise AuthorizationError("Active subscription required")
    return current_user

async def get_tenant_with_permissions(
    tenant_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Tenant:
    tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id,
        Tenant.users.any(User.id == current_user.id)
    ).first()
    
    if not tenant:
        raise AuthorizationError("Tenant not found or access denied")
    
    return tenant
"""
        
        auth_deps_path = os.path.join(project_dir, "src/auth/dependencies.py")
        with open(auth_deps_path, 'w') as f:
            f.write(auth_deps)
    
    def _generate_generic_auth(self, project_dir: str, framework: str, options: Dict):
        """Generate generic authentication system"""
        
        # Generic auth configuration
        auth_config = f"""# Authentication Configuration for {framework}

## Features
- User registration and login
- Password hashing and verification
- JWT token management
- Role-based access control
- Session management
- OAuth integration
- Multi-factor authentication

## Security Features
- Password strength validation
- Account lockout protection
- Rate limiting
- Audit logging
- Session timeout
- CSRF protection

## Configuration
- Authentication provider: {options.get('auth_provider', 'local')}
- Session duration: 30 days
- Password policy: 8+ characters, mixed case, numbers, symbols
- MFA: Optional for users, required for admins

## Implementation Notes
- Use secure password hashing (bcrypt)
- Implement proper session management
- Add rate limiting for auth endpoints
- Log all authentication events
- Use HTTPS in production
"""
        
        auth_config_path = os.path.join(project_dir, "src/auth/README.md")
        with open(auth_config_path, 'w') as f:
            f.write(auth_config)
    
    def _generate_subscription_system(self, project_dir: str, framework: str, options: Dict):
        """Generate subscription management system"""
        logger.info("Generating subscription system...")
        
        if framework == "next":
            self._generate_next_subscriptions(project_dir, options)
        elif framework == "fastapi":
            self._generate_fastapi_subscriptions(project_dir, options)
        else:
            self._generate_generic_subscriptions(project_dir, framework, options)
    
    def _generate_next_subscriptions(self, project_dir: str, options: Dict):
        """Generate Next.js subscription system"""
        
        # Subscription service
        subscription_service = """import { prisma } from '@/lib/prisma'
import { stripe } from '@/lib/stripe'
import { sendEmail } from '@/lib/email'

export interface SubscriptionPlan {
  id: string
  name: string
  price: number
  interval: 'month' | 'year'
  features: string[]
  limits: {
    users: number
    storage: number // in GB
    apiCalls: number
  }
}

export const SUBSCRIPTION_PLANS: SubscriptionPlan[] = [
  {
    id: 'free',
    name: 'Free',
    price: 0,
    interval: 'month',
    features: ['Basic features', 'Community support'],
    limits: {
      users: 1,
      storage: 1,
      apiCalls: 1000,
    },
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 29,
    interval: 'month',
    features: ['All features', 'Priority support', 'Advanced analytics'],
    limits: {
      users: 10,
      storage: 100,
      apiCalls: 10000,
    },
  },
  {
    id: 'team',
    name: 'Team',
    price: 99,
    interval: 'month',
    features: ['Everything in Pro', 'Team collaboration', 'Custom integrations'],
    limits: {
      users: 50,
      storage: 500,
      apiCalls: 50000,
    },
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 299,
    interval: 'month',
    features: ['Everything in Team', 'Dedicated support', 'Custom features'],
    limits: {
      users: -1, // Unlimited
      storage: -1, // Unlimited
      apiCalls: -1, // Unlimited
    },
  },
]

export class SubscriptionService {
  static async createSubscription(
    tenantId: string,
    planId: string,
    userId: string
  ) {
    const tenant = await prisma.tenant.findUnique({
      where: { id: tenantId },
      include: { users: true, subscription: true },
    })

    if (!tenant) {
      throw new Error('Tenant not found')
    }

    const plan = SUBSCRIPTION_PLANS.find(p => p.id === planId)
    if (!plan) {
      throw new Error('Invalid plan')
    }

    // Create Stripe customer if not exists
    let stripeCustomerId = tenant.stripeCustomerId
    if (!stripeCustomerId) {
      const customer = await stripe.customers.create({
        email: tenant.users[0].email,
        name: tenant.name,
        metadata: {
          tenantId: tenant.id,
        },
      })
      stripeCustomerId = customer.id
      
      await prisma.tenant.update({
        where: { id: tenantId },
        data: { stripeCustomerId },
      })
    }

    // Create Stripe subscription
    const subscription = await stripe.subscriptions.create({
      customer: stripeCustomerId,
      items: [{ price: plan.id }],
      trial_period_days: 14,
      metadata: {
        tenantId: tenant.id,
        planId: plan.id,
      },
    })

    // Update tenant subscription
    await prisma.subscription.upsert({
      where: { tenantId },
      update: {
        stripeSubscriptionId: subscription.id,
        status: subscription.status,
        currentPeriodStart: new Date(subscription.current_period_start * 1000),
        currentPeriodEnd: new Date(subscription.current_period_end * 1000),
        plan: planId,
      },
      create: {
        tenantId,
        stripeSubscriptionId: subscription.id,
        status: subscription.status,
        currentPeriodStart: new Date(subscription.current_period_start * 1000),
        currentPeriodEnd: new Date(subscription.current_period_end * 1000),
        plan: planId,
      },
    })

    return subscription
  }

  static async cancelSubscription(tenantId: string) {
    const subscription = await prisma.subscription.findUnique({
      where: { tenantId },
    })

    if (!subscription?.stripeSubscriptionId) {
      throw new Error('No active subscription found')
    }

    // Cancel at period end
    await stripe.subscriptions.update(subscription.stripeSubscriptionId, {
      cancel_at_period_end: true,
    })

    await prisma.subscription.update({
      where: { tenantId },
      data: {
        cancelAtPeriodEnd: true,
      },
    })
  }

  static async updateSubscription(tenantId: string, newPlanId: string) {
    const subscription = await prisma.subscription.findUnique({
      where: { tenantId },
    })

    if (!subscription?.stripeSubscriptionId) {
      throw new Error('No active subscription found')
    }

    const newPlan = SUBSCRIPTION_PLANS.find(p => p.id === newPlanId)
    if (!newPlan) {
      throw new Error('Invalid plan')
    }

    // Update Stripe subscription
    const stripeSubscription = await stripe.subscriptions.retrieve(
      subscription.stripeSubscriptionId
    )

    await stripe.subscriptions.update(subscription.stripeSubscriptionId, {
      items: [
        {
          id: stripeSubscription.items.data[0].id,
          price: newPlan.id,
        },
      ],
      proration_behavior: 'always_invoice',
    })

    await prisma.subscription.update({
      where: { tenantId },
      data: {
        plan: newPlanId,
      },
    })
  }

  static async handleWebhook(event: any) {
    switch (event.type) {
      case 'invoice.payment_succeeded':
        await this.handlePaymentSucceeded(event.data.object)
        break
      case 'invoice.payment_failed':
        await this.handlePaymentFailed(event.data.object)
        break
      case 'customer.subscription.updated':
        await this.handleSubscriptionUpdated(event.data.object)
        break
      case 'customer.subscription.deleted':
        await this.handleSubscriptionDeleted(event.data.object)
        break
    }
  }

  private static async handlePaymentSucceeded(invoice: any) {
    const subscription = await prisma.subscription.findFirst({
      where: { stripeSubscriptionId: invoice.subscription },
      include: { tenant: { include: { users: true } } },
    })

    if (subscription) {
      await prisma.subscription.update({
        where: { id: subscription.id },
        data: { status: 'active' },
      })

      // Send payment confirmation email
      await sendEmail({
        to: subscription.tenant.users[0].email,
        subject: 'Payment Confirmation',
        template: 'payment-success',
        data: {
          amount: invoice.amount_paid / 100,
          currency: invoice.currency,
        },
      })
    }
  }

  private static async handlePaymentFailed(invoice: any) {
    const subscription = await prisma.subscription.findFirst({
      where: { stripeSubscriptionId: invoice.subscription },
      include: { tenant: { include: { users: true } } },
    })

    if (subscription) {
      await prisma.subscription.update({
        where: { id: subscription.id },
        data: { status: 'past_due' },
      })

      // Send payment failure email
      await sendEmail({
        to: subscription.tenant.users[0].email,
        subject: 'Payment Failed',
        template: 'payment-failed',
        data: {
          amount: invoice.amount_due / 100,
          currency: invoice.currency,
        },
      })
    }
  }

  private static async handleSubscriptionUpdated(subscription: any) {
    await prisma.subscription.updateMany({
      where: { stripeSubscriptionId: subscription.id },
      data: {
        status: subscription.status,
        currentPeriodStart: new Date(subscription.current_period_start * 1000),
        currentPeriodEnd: new Date(subscription.current_period_end * 1000),
        cancelAtPeriodEnd: subscription.cancel_at_period_end,
      },
    })
  }

  private static async handleSubscriptionDeleted(subscription: any) {
    await prisma.subscription.updateMany({
      where: { stripeSubscriptionId: subscription.id },
      data: {
        status: 'canceled',
      },
    })
  }

  static async checkLimits(tenantId: string, resource: string, usage: number) {
    const subscription = await prisma.subscription.findUnique({
      where: { tenantId },
    })

    if (!subscription) {
      throw new Error('No subscription found')
    }

    const plan = SUBSCRIPTION_PLANS.find(p => p.id === subscription.plan)
    if (!plan) {
      throw new Error('Invalid plan')
    }

    const limit = plan.limits[resource as keyof typeof plan.limits]
    if (limit !== -1 && usage >= limit) {
      throw new Error(`${resource} limit exceeded`)
    }

    return true
  }
}
"""
        
        subscription_service_path = os.path.join(project_dir, "src/subscriptions/service.ts")
        with open(subscription_service_path, 'w') as f:
            f.write(subscription_service)
    
    def _generate_fastapi_subscriptions(self, project_dir: str, options: Dict):
        """Generate FastAPI subscription system"""
        
        # Subscription models
        subscription_models = """from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), unique=True)
    stripe_subscription_id = Column(String, unique=True)
    status = Column(String, default="active")
    plan = Column(String, default="free")
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="subscription")

class UsageRecord(Base):
    __tablename__ = "usage_records"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.id"))
    resource = Column(String)  # api_calls, storage, users
    usage = Column(Integer, default=0)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tenant = relationship("Tenant")
"""
        
        subscription_models_path = os.path.join(project_dir, "src/subscriptions/models.py")
        with open(subscription_models_path, 'w') as f:
            f.write(subscription_models)
    
    def _generate_generic_subscriptions(self, project_dir: str, framework: str, options: Dict):
        """Generate generic subscription system"""
        
        # Generic subscription configuration
        subscription_config = f"""# Subscription Management System for {framework}

## Features
- Multiple subscription plans (Free, Pro, Team, Enterprise)
- Trial periods and billing cycles
- Usage-based billing
- Subscription upgrades/downgrades
- Automatic billing and invoicing
- Webhook handling for payment events

## Plans Configuration
- Free: Basic features, limited usage
- Pro: Advanced features, higher limits
- Team: Collaboration features, team management
- Enterprise: Custom features, unlimited usage

## Payment Integration
- Provider: {options.get('payment_provider', 'stripe')}
- Billing cycles: Monthly and annual
- Proration: Automatic on plan changes
- Dunning management: Automated retry logic

## Usage Tracking
- API calls per month
- Storage usage in GB
- Number of team members
- Custom feature usage

## Implementation Notes
- Use webhooks for real-time updates
- Implement proper error handling
- Add comprehensive logging
- Test with sandbox environment
- Monitor subscription metrics
"""
        
        subscription_config_path = os.path.join(project_dir, "src/subscriptions/README.md")
        with open(subscription_config_path, 'w') as f:
            f.write(subscription_config)
    
    def _generate_payment_system(self, project_dir: str, framework: str, options: Dict):
        """Generate payment processing system"""
        logger.info("Generating payment system...")
        
        payment_provider = options.get('payment_provider', 'stripe')
        
        if payment_provider == 'stripe':
            self._generate_stripe_integration(project_dir, framework)
        elif payment_provider == 'paddle':
            self._generate_paddle_integration(project_dir, framework)
        else:
            self._generate_generic_payment(project_dir, framework, payment_provider)
    
    def _generate_stripe_integration(self, project_dir: str, framework: str):
        """Generate Stripe integration"""
        
        # Stripe configuration
        stripe_config = """import Stripe from 'stripe'

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
  typescript: true,
})

export const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET!

export const PLANS = {
  free: {
    priceId: 'price_free',
    price: 0,
    name: 'Free',
    description: 'Basic features for individuals',
    features: ['Basic features', 'Community support'],
  },
  pro: {
    priceId: 'price_pro_monthly',
    price: 29,
    name: 'Pro',
    description: 'Advanced features for professionals',
    features: ['All features', 'Priority support', 'Advanced analytics'],
  },
  team: {
    priceId: 'price_team_monthly',
    price: 99,
    name: 'Team',
    description: 'Collaboration features for teams',
    features: ['Everything in Pro', 'Team collaboration', 'Custom integrations'],
  },
  enterprise: {
    priceId: 'price_enterprise_monthly',
    price: 299,
    name: 'Enterprise',
    description: 'Custom solutions for large organizations',
    features: ['Everything in Team', 'Dedicated support', 'Custom features'],
  },
}
"""
        
        stripe_config_path = os.path.join(project_dir, "src/payments/stripe.ts")
        with open(stripe_config_path, 'w') as f:
            f.write(stripe_config)
        
        # Stripe webhook handler
        webhook_handler = """import { NextRequest, NextResponse } from 'next/server'
import { stripe, STRIPE_WEBHOOK_SECRET } from '@/lib/stripe'
import { SubscriptionService } from '@/services/subscription'

export async function POST(request: NextRequest) {
  const body = await request.text()
  const signature = request.headers.get('stripe-signature')

  if (!signature) {
    return NextResponse.json({ error: 'No signature' }, { status: 400 })
  }

  let event: any

  try {
    event = stripe.webhooks.constructEvent(body, signature, STRIPE_WEBHOOK_SECRET)
  } catch (err) {
    console.error('Webhook signature verification failed:', err)
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  try {
    await SubscriptionService.handleWebhook(event)
    return NextResponse.json({ received: true })
  } catch (error) {
    console.error('Webhook handler failed:', error)
    return NextResponse.json({ error: 'Webhook handler failed' }, { status: 500 })
  }
}
"""
        
        webhook_path = os.path.join(project_dir, "src/api/webhooks/stripe/route.ts")
        os.makedirs(os.path.dirname(webhook_path), exist_ok=True)
        with open(webhook_path, 'w') as f:
            f.write(webhook_handler)
    
    def _generate_paddle_integration(self, project_dir: str, framework: str):
        """Generate Paddle integration"""
        
        # Paddle configuration
        paddle_config = """// Paddle Integration Configuration
export const PADDLE_VENDOR_ID = process.env.PADDLE_VENDOR_ID
export const PADDLE_WEBHOOK_SECRET = process.env.PADDLE_WEBHOOK_SECRET
export const PADDLE_API_KEY = process.env.PADDLE_API_KEY
export const PADDLE_ENVIRONMENT = process.env.PADDLE_ENVIRONMENT || 'sandbox'

export const PADDLE_PLANS = {
  pro: {
    planId: 'paddle_pro_plan_id',
    price: 29,
    name: 'Pro',
    description: 'Advanced features for professionals',
  },
  team: {
    planId: 'paddle_team_plan_id',
    price: 99,
    name: 'Team',
    description: 'Collaboration features for teams',
  },
  enterprise: {
    planId: 'paddle_enterprise_plan_id',
    price: 299,
    name: 'Enterprise',
    description: 'Custom solutions for large organizations',
  },
}

export async function createPaddleCheckout(planId: string, customerEmail: string) {
  // Paddle checkout implementation
  const checkoutData = {
    vendor_id: PADDLE_VENDOR_ID,
    product_id: planId,
    customer_email: customerEmail,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard`,
    webhook_url: `${process.env.NEXT_PUBLIC_APP_URL}/api/webhooks/paddle`,
  }

  // Return checkout URL or embed code
  return checkoutData
}
"""
        
        paddle_config_path = os.path.join(project_dir, "src/payments/paddle.ts")
        with open(paddle_config_path, 'w') as f:
            f.write(paddle_config)
    
    def _generate_generic_payment(self, project_dir: str, framework: str, provider: str):
        """Generate generic payment integration"""
        
        # Generic payment configuration
        payment_config = f"""# Payment Integration for {provider}

## Configuration
- Provider: {provider}
- Environment: Sandbox/Production
- Webhook URL: /api/webhooks/{provider}
- Return URL: /dashboard

## Features
- Subscription creation and management
- Payment processing
- Webhook handling
- Billing management
- Invoice generation

## Security
- Webhook signature verification
- Secure API key storage
- PCI compliance
- Fraud protection

## Implementation Notes
- Use environment variables for sensitive data
- Implement proper error handling
- Add comprehensive logging
- Test with sandbox environment
- Monitor payment metrics
"""
        
        payment_config_path = os.path.join(project_dir, "src/payments/README.md")
        with open(payment_config_path, 'w') as f:
            f.write(payment_config)
    
    def _generate_multi_tenant_system(self, project_dir: str, framework: str, options: Dict):
        """Generate multi-tenant architecture"""
        logger.info("Generating multi-tenant system...")
        
        # Database schema for multi-tenancy
        if framework == "next":
            self._generate_prisma_schema(project_dir, options)
        elif framework == "fastapi":
            self._generate_sqlalchemy_models(project_dir, options)
        else:
            self._generate_generic_tenant_schema(project_dir, framework, options)
    
    def _generate_prisma_schema(self, project_dir: str, options: Dict):
        """Generate Prisma schema for multi-tenancy"""
        
        prisma_schema = """generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Tenant {
  id                String   @id @default(cuid())
  name              String
  slug              String   @unique
  domain            String?  @unique
  logo              String?
  plan              String   @default("free")
  status            String   @default("active")
  stripeCustomerId  String?  @unique
  settings          Json?
  trialEndsAt       DateTime?
  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt

  users        User[]
  subscription Subscription?
  apiKeys      ApiKey[]
  usage        UsageRecord[]
  auditLogs    AuditLog[]

  @@map("tenants")
}

model User {
  id                String    @id @default(cuid())
  email             String    @unique
  name              String?
  image             String?
  role              String    @default("member")
  status            String    @default("active")
  emailVerified     DateTime?
  lastLoginAt       DateTime?
  subscriptionStatus String?
  tenantId          String
  createdAt         DateTime  @default(now())
  updatedAt         DateTime  @updatedAt

  tenant   Tenant    @relation(fields: [tenantId], references: [id], onDelete: Cascade)
  accounts Account[]
  sessions Session[]

  @@map("users")
}

model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
  @@map("accounts")
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("sessions")
}

model VerificationToken {
  identifier String
  token      String   @unique
  expires    DateTime

  @@unique([identifier, token])
  @@map("verification_tokens")
}

model Subscription {
  id                    String   @id @default(cuid())
  tenantId              String   @unique
  stripeSubscriptionId  String?  @unique
  status                String   @default("active")
  plan                  String   @default("free")
  currentPeriodStart    DateTime?
  currentPeriodEnd      DateTime?
  cancelAtPeriodEnd     Boolean  @default(false)
  createdAt             DateTime @default(now())
  updatedAt             DateTime @updatedAt

  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)

  @@map("subscriptions")
}

model ApiKey {
  id        String   @id @default(cuid())
  name      String
  key       String   @unique
  tenantId  String
  scopes    String[]
  lastUsed  DateTime?
  expiresAt DateTime?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)

  @@map("api_keys")
}

model UsageRecord {
  id          String   @id @default(cuid())
  tenantId    String
  resource    String   // api_calls, storage, users
  usage       Int      @default(0)
  periodStart DateTime
  periodEnd   DateTime
  createdAt   DateTime @default(now())

  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)

  @@map("usage_records")
}

model AuditLog {
  id        String   @id @default(cuid())
  tenantId  String
  userId    String?
  action    String
  resource  String
  details   Json?
  ipAddress String?
  userAgent String?
  createdAt DateTime @default(now())

  tenant Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)

  @@map("audit_logs")
}
"""
        
        prisma_schema_path = os.path.join(project_dir, "prisma/schema.prisma")
        os.makedirs(os.path.dirname(prisma_schema_path), exist_ok=True)
        with open(prisma_schema_path, 'w') as f:
            f.write(prisma_schema)
    
    def _generate_sqlalchemy_models(self, project_dir: str, options: Dict):
        """Generate SQLAlchemy models for multi-tenancy"""
        
        models = """from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    domain = Column(String, unique=True)
    logo = Column(String)
    plan = Column(String, default="free")
    status = Column(String, default="active")
    stripe_customer_id = Column(String, unique=True)
    settings = Column(JSON)
    trial_ends_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    users = relationship("User", back_populates="tenant")
    subscription = relationship("Subscription", back_populates="tenant", uselist=False)
    api_keys = relationship("ApiKey", back_populates="tenant")
    usage_records = relationship("UsageRecord", back_populates="tenant")
    audit_logs = relationship("AuditLog", back_populates="tenant")

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    image = Column(String)
    role = Column(String, default="member")
    status = Column(String, default="active")
    email_verified = Column(DateTime)
    last_login_at = Column(DateTime)
    subscription_status = Column(String)
    tenant_id = Column(String, ForeignKey("tenants.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="users")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(String, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), unique=True)
    stripe_subscription_id = Column(String, unique=True)
    status = Column(String, default="active")
    plan = Column(String, default="free")
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="subscription")

class ApiKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    key = Column(String, unique=True, nullable=False)
    tenant_id = Column(String, ForeignKey("tenants.id"))
    scopes = Column(JSON)
    last_used = Column(DateTime)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="api_keys")

class UsageRecord(Base):
    __tablename__ = "usage_records"
    
    id = Column(String, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.id"))
    resource = Column(String, nullable=False)
    usage = Column(Integer, default=0)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="usage_records")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.id"))
    user_id = Column(String)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    details = Column(JSON)
    ip_address = Column(String)
    user_agent = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="audit_logs")
"""
        
        models_path = os.path.join(project_dir, "src/models/database.py")
        with open(models_path, 'w') as f:
            f.write(models)
    
    def _generate_generic_tenant_schema(self, project_dir: str, framework: str, options: Dict):
        """Generate generic tenant schema"""
        
        schema_config = f"""# Multi-Tenant Database Schema for {framework}

## Tables

### Tenants
- id (primary key)
- name
- slug (unique)
- domain (optional, unique)
- plan (free, pro, team, enterprise)
- status (active, suspended, canceled)
- settings (JSON)
- created_at, updated_at

### Users
- id (primary key)
- email (unique)
- name
- role (owner, admin, member)
- tenant_id (foreign key)
- status (active, inactive, invited)
- created_at, updated_at

### Subscriptions
- id (primary key)
- tenant_id (foreign key, unique)
- stripe_subscription_id
- status (active, past_due, canceled)
- plan
- current_period_start, current_period_end
- created_at, updated_at

### API Keys
- id (primary key)
- tenant_id (foreign key)
- name
- key (unique)
- scopes (JSON array)
- last_used
- expires_at
- created_at, updated_at

### Usage Records
- id (primary key)
- tenant_id (foreign key)
- resource (api_calls, storage, users)
- usage (integer)
- period_start, period_end
- created_at

### Audit Logs
- id (primary key)
- tenant_id (foreign key)
- user_id
- action
- resource
- details (JSON)
- ip_address
- user_agent
- created_at

## Indexes
- tenants.slug
- users.email
- users.tenant_id
- subscriptions.tenant_id
- api_keys.key
- usage_records.tenant_id, period_start
- audit_logs.tenant_id, created_at

## Implementation Notes
- Use row-level security for tenant isolation
- Implement proper foreign key constraints
- Add database migrations
- Use connection pooling
- Monitor query performance
"""
        
        schema_path = os.path.join(project_dir, "src/database/schema.md")
        os.makedirs(os.path.dirname(schema_path), exist_ok=True)
        with open(schema_path, 'w') as f:
            f.write(schema_config)
    
    def _generate_admin_dashboard(self, project_dir: str, framework: str, options: Dict):
        """Generate admin dashboard"""
        logger.info("Generating admin dashboard...")
        
        # Admin dashboard configuration
        admin_config = f"""# Admin Dashboard Configuration

## Features
- User management
- Tenant management
- Subscription management
- Usage analytics
- System monitoring
- Audit logs
- Configuration management

## Access Control
- Admin role required
- IP whitelist (optional)
- Multi-factor authentication
- Session timeout
- Activity logging

## Dashboard Sections
- Overview with key metrics
- User management (CRUD operations)
- Tenant management (status, settings)
- Subscription management (plans, billing)
- Analytics (usage, revenue, growth)
- System health (performance, errors)
- Audit logs (security, compliance)

## Security Features
- Role-based access control
- Audit logging for all actions
- Secure API endpoints
- Rate limiting
- Input validation
- CSRF protection

## Implementation Notes
- Use secure authentication
- Implement proper authorization
- Add comprehensive logging
- Monitor admin activities
- Regular security audits
"""
        
        admin_config_path = os.path.join(project_dir, "src/admin/README.md")
        with open(admin_config_path, 'w') as f:
            f.write(admin_config)
    
    def _generate_api_management(self, project_dir: str, framework: str, options: Dict):
        """Generate API management system"""
        logger.info("Generating API management...")
        
        # API configuration
        api_config = f"""# API Management System

## Features
- API key management
- Rate limiting
- Request/response logging
- API documentation
- Versioning
- Webhooks

## Authentication
- API key authentication
- JWT tokens
- OAuth 2.0 (optional)
- Rate limiting per key

## Rate Limiting
- Per-tenant limits
- Per-endpoint limits
- Burst protection
- Graceful degradation

## Monitoring
- Request metrics
- Error tracking
- Performance monitoring
- Usage analytics

## Documentation
- Auto-generated API docs
- Interactive API explorer
- SDKs for popular languages
- Code examples

## Implementation Notes
- Use middleware for authentication
- Implement proper error handling
- Add comprehensive logging
- Monitor API performance
- Version your APIs properly
"""
        
        api_config_path = os.path.join(project_dir, "src/api/README.md")
        with open(api_config_path, 'w') as f:
            f.write(api_config)
    
    def _generate_analytics_system(self, project_dir: str, framework: str, options: Dict):
        """Generate analytics system"""
        logger.info("Generating analytics system...")
        
        # Analytics configuration
        analytics_config = f"""# Analytics System

## Business Metrics
- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (CLV)
- Churn Rate
- Trial Conversion Rate
- Feature Usage

## User Analytics
- User registration and onboarding
- Feature adoption rates
- User engagement metrics
- Retention cohorts
- Usage patterns

## Technical Metrics
- API usage statistics
- Performance metrics
- Error rates
- System health
- Resource utilization

## Implementation
- Event tracking
- Data aggregation
- Real-time dashboards
- Automated reporting
- Alert system

## Tools Integration
- Mixpanel for user analytics
- Segment for data routing
- PostHog for product analytics
- Custom metrics dashboard

## Privacy
- GDPR compliance
- Data anonymization
- Consent management
- Data retention policies

## Implementation Notes
- Use event-driven architecture
- Implement proper data governance
- Add privacy controls
- Monitor data quality
- Regular reporting
"""
        
        analytics_config_path = os.path.join(project_dir, "src/analytics/README.md")
        with open(analytics_config_path, 'w') as f:
            f.write(analytics_config)
    
    def _generate_monitoring_system(self, project_dir: str, framework: str, options: Dict):
        """Generate monitoring and logging system"""
        logger.info("Generating monitoring system...")
        
        # Monitoring configuration
        monitoring_config = f"""# Monitoring and Logging System

## Application Monitoring
- Health checks
- Performance metrics
- Error tracking
- Uptime monitoring
- Resource utilization

## Business Monitoring
- Revenue tracking
- User activity
- Conversion funnels
- Churn indicators
- Growth metrics

## Security Monitoring
- Authentication failures
- Suspicious activities
- API abuse
- Data access patterns
- Compliance violations

## Alert System
- Real-time alerts
- Escalation rules
- Multiple channels (email, Slack, SMS)
- Alert fatigue prevention
- Automated responses

## Logging
- Structured logging
- Centralized log management
- Log retention policies
- Search and analysis
- Audit trails

## Tools Integration
- Sentry for error tracking
- DataDog for monitoring
- LogRocket for user sessions
- PagerDuty for incident management

## Implementation Notes
- Use structured logging
- Implement proper alerting
- Monitor key metrics
- Regular system health checks
- Incident response procedures
"""
        
        monitoring_config_path = os.path.join(project_dir, "src/monitoring/README.md")
        with open(monitoring_config_path, 'w') as f:
            f.write(monitoring_config)
    
    def _generate_deployment_config(self, project_dir: str, framework: str, options: Dict):
        """Generate deployment configuration"""
        logger.info("Generating deployment configuration...")
        
        # Docker configuration
        if framework == "next":
            dockerfile_content = self._get_next_dockerfile()
        elif framework == "fastapi":
            dockerfile_content = self._get_fastapi_dockerfile()
        else:
            dockerfile_content = self._get_generic_saas_dockerfile()
        
        dockerfile_path = os.path.join(project_dir, "Dockerfile")
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        # Docker compose for development
        docker_compose_content = self._get_saas_docker_compose(framework, options)
        
        compose_path = os.path.join(project_dir, "docker-compose.yml")
        with open(compose_path, 'w') as f:
            f.write(docker_compose_content)
        
        # Kubernetes configuration
        k8s_config = self._get_kubernetes_config(framework, options)
        
        k8s_dir = os.path.join(project_dir, "k8s")
        os.makedirs(k8s_dir, exist_ok=True)
        
        k8s_path = os.path.join(k8s_dir, "deployment.yaml")
        with open(k8s_path, 'w') as f:
            f.write(k8s_config)
    
    def _get_next_dockerfile(self) -> str:
        """Get Next.js Dockerfile for SaaS"""
        return """# Multi-stage build for Next.js SaaS application
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \\
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \\
  elif [ -f package-lock.json ]; then npm ci; \\
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i --frozen-lockfile; \\
  else echo "Lockfile not found." && exit 1; \\
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Generate Prisma client
RUN npx prisma generate

# Build the application
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Copy Prisma schema and client
COPY --from=builder --chown=nextjs:nodejs /app/prisma ./prisma
COPY --from=builder --chown=nextjs:nodejs /app/node_modules/.prisma ./node_modules/.prisma

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
"""
    
    def _get_fastapi_dockerfile(self) -> str:
        """Get FastAPI Dockerfile for SaaS"""
        return """# FastAPI SaaS Application
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    curl \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY requirements-prod.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' --uid 1001 appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
"""
    
    def _get_generic_saas_dockerfile(self) -> str:
        """Get generic SaaS Dockerfile"""
        return """# Generic SaaS Application
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build application
RUN npm run build

# Create non-root user
RUN addgroup -g 1001 -S appuser && adduser -S appuser -u 1001

# Change ownership
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:3000/health || exit 1

# Start application
CMD ["npm", "start"]
"""
    
    def _get_saas_docker_compose(self, framework: str, options: Dict) -> str:
        """Get Docker Compose for SaaS development"""
        database = options.get('database', 'postgresql')
        
        return f"""version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://saas:password@db:5432/saas_dev
      - REDIS_URL=redis://redis:6379
      - STRIPE_SECRET_KEY=sk_test_...
      - NEXTAUTH_SECRET=your-secret-key
      - NEXTAUTH_URL=http://localhost:3000
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
      - /app/node_modules
    command: npm run dev

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=saas_dev
      - POSTGRES_USER=saas
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"
      - "8025:8025"

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
"""
    
    def _get_kubernetes_config(self, framework: str, options: Dict) -> str:
        """Get Kubernetes configuration for SaaS"""
        return """apiVersion: apps/v1
kind: Deployment
metadata:
  name: saas-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: saas-app
  template:
    metadata:
      labels:
        app: saas-app
    spec:
      containers:
      - name: app
        image: saas-app:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: saas-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: saas-secrets
              key: redis-url
        - name: STRIPE_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: saas-secrets
              key: stripe-secret-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: saas-app-service
  namespace: production
spec:
  selector:
    app: saas-app
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: saas-app-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - yoursaas.com
    secretName: saas-tls
  rules:
  - host: yoursaas.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: saas-app-service
            port:
              number: 80
"""
    
    def _generate_saas_documentation(self, project_dir: str, name: str, framework: str, options: Dict):
        """Generate comprehensive SaaS documentation"""
        logger.info("Generating SaaS documentation...")
        
        # Business documentation
        business_doc = f"""# {name} - SaaS Business Documentation

## Executive Summary

{name} is a modern SaaS application built with {framework} that provides [describe your service].

## Business Model

### Target Market
- Primary: [Define primary target market]
- Secondary: [Define secondary target market]
- Market Size: [Estimate market size]

### Value Proposition
- Problem: [What problem does your SaaS solve?]
- Solution: [How does your SaaS solve it?]
- Unique Value: [What makes your SaaS unique?]

### Subscription Plans

#### Free Plan
- Price: $0/month
- Features: Basic features for individuals
- Limits: 1 user, 1GB storage, 1,000 API calls/month

#### Pro Plan
- Price: $29/month
- Features: Advanced features for professionals
- Limits: 10 users, 100GB storage, 10,000 API calls/month

#### Team Plan
- Price: $99/month
- Features: Collaboration features for teams
- Limits: 50 users, 500GB storage, 50,000 API calls/month

#### Enterprise Plan
- Price: $299/month
- Features: Custom solutions for large organizations
- Limits: Unlimited users, storage, and API calls

## Key Performance Indicators (KPIs)

### Financial Metrics
- Monthly Recurring Revenue (MRR)
- Annual Recurring Revenue (ARR)
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (CLV)
- Gross Revenue Retention
- Net Revenue Retention

### Product Metrics
- Monthly Active Users (MAU)
- Daily Active Users (DAU)
- Feature Adoption Rate
- User Engagement Score
- Trial-to-Paid Conversion Rate
- Churn Rate

### Operational Metrics
- Customer Support Response Time
- System Uptime
- API Performance
- Security Incident Response Time

## Growth Strategy

### Customer Acquisition
- Content marketing
- SEO optimization
- Social media marketing
- Paid advertising
- Referral programs
- Partnership channels

### Customer Retention
- Onboarding optimization
- Feature adoption campaigns
- Customer success programs
- Regular product updates
- Community building

### Revenue Growth
- Plan upgrades
- Usage-based billing
- Add-on features
- Annual plan discounts
- Enterprise sales

## Competitive Analysis

### Direct Competitors
- [Competitor 1]: [Strengths and weaknesses]
- [Competitor 2]: [Strengths and weaknesses]
- [Competitor 3]: [Strengths and weaknesses]

### Competitive Advantages
- [Advantage 1]: [Description]
- [Advantage 2]: [Description]
- [Advantage 3]: [Description]

## Risk Assessment

### Technical Risks
- System downtime
- Data security breaches
- Scalability challenges
- Integration failures

### Business Risks
- Market competition
- Economic downturns
- Regulatory changes
- Customer churn

### Mitigation Strategies
- Robust monitoring systems
- Security best practices
- Scalable architecture
- Diversified revenue streams

## Financial Projections

### Year 1 Targets
- MRR: $10,000
- Customers: 500
- Churn Rate: <10%
- CAC Payback: <12 months

### Year 2 Targets
- MRR: $50,000
- Customers: 2,000
- Churn Rate: <7%
- CAC Payback: <9 months

### Year 3 Targets
- MRR: $200,000
- Customers: 5,000
- Churn Rate: <5%
- CAC Payback: <6 months

## Technology Stack

### Frontend
- Framework: {framework}
- Language: TypeScript
- UI Library: Tailwind CSS
- State Management: Redux/Zustand

### Backend
- Runtime: Node.js
- Database: PostgreSQL
- Cache: Redis
- Authentication: NextAuth.js

### Infrastructure
- Hosting: Vercel/AWS
- Database: Supabase/AWS RDS
- Monitoring: Sentry/DataDog
- Analytics: Mixpanel/PostHog

### AI Enhancement
- CEO Quality Control Agent
- Sequential thinking for strategic decisions
- Perplexity for market research
- Automated testing and deployment

## Next Steps

1. Complete MVP development
2. Beta testing with select customers
3. Launch marketing campaigns
4. Gather user feedback
5. Iterate and improve
6. Scale operations
7. Expand feature set
8. International expansion
"""
        
        business_doc_path = os.path.join(project_dir, "docs/business-plan.md")
        with open(business_doc_path, 'w') as f:
            f.write(business_doc)
        
        # Technical documentation
        tech_doc = f"""# {name} - Technical Documentation

## Architecture Overview

{name} is built as a multi-tenant SaaS application using modern web technologies and AI-powered development tools.

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   ({framework}) │◄───┤   API Server    │◄───┤   PostgreSQL    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CDN/Assets    │    │   Background    │    │   Cache Layer   │
│   (Vercel)      │    │   Jobs (Queue)  │    │   (Redis)       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Multi-Tenant Architecture

- **Tenant Isolation**: Schema-based isolation with row-level security
- **Data Partitioning**: Logical separation by tenant_id
- **Resource Quotas**: Per-tenant limits on storage, API calls, users
- **Custom Domains**: Optional custom domain support

### Security

- **Authentication**: OAuth 2.0 with multiple providers
- **Authorization**: Role-based access control (RBAC)
- **Data Encryption**: AES-256 at rest, TLS 1.3 in transit
- **API Security**: Rate limiting, input validation, CORS
- **Compliance**: SOC 2 Type II, GDPR, CCPA

### Scalability

- **Horizontal Scaling**: Load balancing across multiple instances
- **Database Scaling**: Read replicas, connection pooling
- **Caching**: Redis for session storage and API responses
- **CDN**: Global content delivery network
- **Monitoring**: Real-time performance monitoring

## Development Workflow

### AI-Enhanced Development

The project uses AI-powered development tools for enhanced productivity:

1. **CEO Quality Control Agent**: Monitors code quality and enforces standards
2. **Sequential Thinking**: Assists with complex problem-solving
3. **Perplexity Integration**: Provides real-time research and insights
4. **Automated Testing**: Playwright for end-to-end testing
5. **Continuous Integration**: GitHub Actions with quality gates

### Development Process

1. **Planning**: Use Sequential Thinking for feature planning
2. **Research**: Perplexity for competitive analysis and best practices
3. **Development**: Code with AI assistance and real-time feedback
4. **Quality Control**: Automatic code review by CEO Agent
5. **Testing**: Automated testing with Playwright
6. **Deployment**: Continuous deployment with quality gates

### Code Quality Standards

- **Test Coverage**: Minimum 80% code coverage
- **Code Review**: All code reviewed by CEO Quality Control Agent
- **Linting**: ESLint with TypeScript rules
- **Formatting**: Prettier with consistent formatting
- **Security**: Automated security scanning

## API Documentation

### Authentication

All API requests require authentication using JWT tokens:

```
Authorization: Bearer <your-jwt-token>
```

### Rate Limiting

API requests are rate-limited based on subscription plan:

- Free: 1,000 requests/month
- Pro: 10,000 requests/month
- Team: 50,000 requests/month
- Enterprise: Unlimited

### Core Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - User logout

#### Tenants
- `GET /api/tenants` - List user's tenants
- `POST /api/tenants` - Create new tenant
- `GET /api/tenants/:id` - Get tenant details
- `PUT /api/tenants/:id` - Update tenant
- `DELETE /api/tenants/:id` - Delete tenant

#### Users
- `GET /api/users` - List tenant users
- `POST /api/users` - Invite user
- `GET /api/users/:id` - Get user details
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Remove user

#### Subscriptions
- `GET /api/subscriptions` - Get subscription details
- `POST /api/subscriptions` - Create subscription
- `PUT /api/subscriptions` - Update subscription
- `DELETE /api/subscriptions` - Cancel subscription

### Webhooks

#### Stripe Webhooks
- `POST /api/webhooks/stripe` - Handle Stripe events

#### Custom Webhooks
- `POST /api/webhooks/custom` - Handle custom events

## Database Schema

### Core Tables

#### Tenants
```sql
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  domain VARCHAR(255) UNIQUE,
  plan VARCHAR(50) DEFAULT 'free',
  status VARCHAR(50) DEFAULT 'active',
  settings JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Users
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  role VARCHAR(50) DEFAULT 'member',
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Subscriptions
```sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID UNIQUE REFERENCES tenants(id) ON DELETE CASCADE,
  stripe_subscription_id VARCHAR(255) UNIQUE,
  status VARCHAR(50) DEFAULT 'active',
  plan VARCHAR(50) DEFAULT 'free',
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Indexes

```sql
CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_subscriptions_tenant_id ON subscriptions(tenant_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
```

## Deployment

### Development Environment

```bash
# Install dependencies
npm install

# Setup environment variables
cp .env.example .env

# Run database migrations
npx prisma migrate dev

# Start development server
npm run dev
```

### Production Deployment

#### Docker
```bash
# Build image
docker build -t saas-app .

# Run container
docker run -p 3000:3000 saas-app
```

#### Kubernetes
```bash
# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml

# Check deployment status
kubectl get pods -l app=saas-app
```

### Environment Variables

```bash
# Application
NEXTAUTH_URL=https://yoursaas.com
NEXTAUTH_SECRET=your-secret-key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/saas

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
SENDGRID_API_KEY=SG...

# Analytics
MIXPANEL_TOKEN=...
```

## Monitoring and Logging

### Health Checks
- `GET /api/health` - Application health
- `GET /api/health/db` - Database health
- `GET /api/health/redis` - Redis health

### Metrics
- Application performance metrics
- Business metrics (MRR, churn, etc.)
- System metrics (CPU, memory, etc.)
- User behavior analytics

### Alerting
- System alerts for downtime
- Performance alerts for slow responses
- Business alerts for key metrics
- Security alerts for suspicious activity

## Security

### Authentication Flow
1. User initiates login
2. OAuth provider authentication
3. JWT token generation
4. Session management
5. Token refresh handling

### Authorization
- Role-based access control (RBAC)
- Resource-level permissions
- Tenant-based isolation
- API key authentication

### Data Protection
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Data anonymization
- Secure data deletion

### Compliance
- SOC 2 Type II compliance
- GDPR compliance
- CCPA compliance
- Regular security audits

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database connection
npx prisma db pull

# Reset database
npx prisma migrate reset
```

#### Authentication Issues
```bash
# Check JWT token
jwt.io

# Verify OAuth configuration
```

#### Payment Issues
```bash
# Check Stripe webhook logs
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Test payment flows
```

### Performance Optimization

#### Database Optimization
- Add appropriate indexes
- Optimize query performance
- Use connection pooling
- Implement caching

#### Frontend Optimization
- Code splitting
- Image optimization
- Bundle optimization
- CDN usage

#### API Optimization
- Response caching
- Rate limiting
- Pagination
- Compression

## Support

### Documentation
- API documentation: `/docs/api`
- User guides: `/docs/user`
- Developer resources: `/docs/developer`

### Community
- Discord server: [Link]
- GitHub discussions: [Link]
- Stack Overflow: [Tag]

### Enterprise Support
- Dedicated support team
- SLA guarantees
- Custom integrations
- On-premises deployment

For technical issues, please create an issue in the GitHub repository or contact our support team.
"""
        
        tech_doc_path = os.path.join(project_dir, "docs/technical-documentation.md")
        with open(tech_doc_path, 'w') as f:
            f.write(tech_doc)
    
    def _generate_ai_integration(self, project_dir: str, name: str, framework: str, options: Dict):
        """Generate AI integration for SaaS"""
        logger.info("Generating AI integration...")
        
        # Copy CEO Quality Control Agent for SaaS
        ceo_agent_source = "/mnt/c/bmad-workspace/ceo-quality-control-agent.py"
        ceo_agent_dest = os.path.join(project_dir, "scripts/ceo-quality-control-agent.py")
        
        if os.path.exists(ceo_agent_source):
            shutil.copy2(ceo_agent_source, ceo_agent_dest)
        
        # SaaS-specific AI configuration
        ai_config = {
            "saas_ai_features": {
                "customer_insights": "AI-powered customer behavior analysis",
                "churn_prediction": "Machine learning churn prediction",
                "pricing_optimization": "AI-driven pricing recommendations",
                "support_automation": "Automated customer support",
                "content_generation": "AI-generated marketing content",
                "feature_recommendations": "AI-powered feature suggestions"
            },
            "business_intelligence": {
                "revenue_forecasting": "AI-powered revenue predictions",
                "market_analysis": "Automated competitive analysis",
                "user_segmentation": "AI-based user clustering",
                "growth_optimization": "AI-driven growth strategies"
            },
            "automation": {
                "onboarding": "Automated user onboarding",
                "billing": "Intelligent billing management",
                "notifications": "Smart notification system",
                "reporting": "Automated business reporting"
            }
        }
        
        ai_config_path = os.path.join(project_dir, "config/ai-config.yaml")
        with open(ai_config_path, 'w') as f:
            yaml.dump(ai_config, f)
    
    def _initialize_git(self, project_dir: str):
        """Initialize git repository"""
        try:
            os.chdir(project_dir)
            
            # Initialize git
            subprocess.run(["git", "init"], check=True)
            
            # Add all files
            subprocess.run(["git", "add", "."], check=True)
            
            # Initial commit
            subprocess.run([
                "git", "commit", "-m", "🚀 Initial commit: SaaS application with AI development tools"
            ], check=True)
            
            logger.info("✅ Git repository initialized")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initialize git: {e}")
        except Exception as e:
            logger.error(f"Error initializing git: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate SaaS application')
    parser.add_argument('--name', required=True, help='SaaS application name')
    parser.add_argument('--framework', required=True, 
                       choices=['next', 'nuxt', 'remix', 'sveltekit', 'fastapi'],
                       help='Framework to use')
    parser.add_argument('--database', default='postgresql',
                       choices=['postgresql', 'mongodb', 'supabase'],
                       help='Database to use')
    parser.add_argument('--payment-provider', default='stripe',
                       choices=['stripe', 'paddle', 'lemonsqueezy'],
                       help='Payment provider')
    parser.add_argument('--auth-provider', default='next-auth',
                       choices=['next-auth', 'auth0', 'supabase-auth'],
                       help='Authentication provider')
    parser.add_argument('--features', nargs='+', 
                       choices=list(SaaSAppTemplateGenerator().saas_features.keys()),
                       help='Additional SaaS features to include')
    
    args = parser.parse_args()
    
    # Validate framework
    generator = SaaSAppTemplateGenerator()
    
    if args.framework not in generator.saas_frameworks:
        logger.error(f"Invalid framework: {args.framework}")
        sys.exit(1)
    
    # Generate SaaS application
    options = {
        'database': args.database,
        'payment_provider': args.payment_provider,
        'auth_provider': args.auth_provider,
        'features': args.features or []
    }
    
    try:
        project_dir = generator.generate_saas_app(args.name, args.framework, options)
        
        logger.info(f"""
🎉 SaaS application '{args.name}' generated successfully!

📁 Location: {project_dir}
🎯 Framework: {args.framework}
💳 Payment Provider: {args.payment_provider}
🔐 Auth Provider: {args.auth_provider}
🗄️ Database: {args.database}

🚀 SaaS Features:
- Multi-tenant architecture
- Subscription management
- Payment processing
- User authentication
- Admin dashboard
- Analytics and monitoring
- API management
- AI-powered development

🧠 AI Enhancement:
- CEO Quality Control Agent
- Sequential thinking for business decisions
- Perplexity for market research
- Automated testing and deployment
- Performance optimization

📋 Next Steps:
1. cd {project_dir}
2. Configure environment variables
3. Run database migrations
4. Start the CEO Quality Control Agent
5. Begin development with AI assistance!

📚 Documentation:
- Business Plan: docs/business-plan.md
- Technical Docs: docs/technical-documentation.md
- API Docs: docs/api-documentation.md
- CLAUDE.md: AI configuration

🎯 Business Metrics to Track:
- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (CLV)
- Churn Rate
- Trial Conversion Rate

Your AI-powered SaaS application is ready for rapid development and scaling! 🚀
""")
        
    except Exception as e:
        logger.error(f"Failed to generate SaaS application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()