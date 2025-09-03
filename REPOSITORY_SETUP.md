# 🚀 Repository Setup Guide

This guide will help you set up a remote repository for the Alrouf Quotation Microservice project.

## 📋 Prerequisites

- Git installed on your system
- GitHub/GitLab/Bitbucket account
- SSH key configured (recommended) or Personal Access Token

## 🔧 Step-by-Step Setup

### 1. Create Remote Repository

#### **Option A: GitHub (Recommended)**
1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the repository details:
   - **Repository name**: `alrouf-quotation-microservice`
   - **Description**: `FastAPI-based quotation microservice for Alrouf Lighting Technology evaluation task`
   - **Visibility**: Choose Public or Private
   - **Initialize with**: Leave unchecked (we already have files)
5. Click "Create repository"

#### **Option B: GitLab**
1. Go to [GitLab.com](https://gitlab.com) and sign in
2. Click "New project"
3. Choose "Create blank project"
4. Fill in project details and click "Create project"

#### **Option C: Bitbucket**
1. Go to [Bitbucket.org](https://bitbucket.org) and sign in
2. Click "Create repository"
3. Fill in repository details and click "Create repository"

### 2. Add Remote Origin

After creating the remote repository, you'll see setup instructions. Use one of these commands:

#### **HTTPS (if using Personal Access Token)**
```bash
git remote add origin https://github.com/YOUR_USERNAME/alrouf-quotation-microservice.git
```

#### **SSH (if using SSH key)**
```bash
git remote add origin git@github.com:YOUR_USERNAME/alrouf-quotation-microservice.git
```

### 3. Push to Remote Repository

```bash
# Push the main branch
git push -u origin main

# Verify remote is added
git remote -v
```

### 4. Set Up Branch Protection (Optional but Recommended)

#### **GitHub:**
1. Go to your repository → Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

#### **GitLab:**
1. Go to your project → Settings → Repository
2. Expand "Protected branches"
3. Protect `main` branch with appropriate rules

## 🔐 Authentication Setup

### **SSH Key Setup (Recommended)**

1. **Generate SSH key:**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **Add SSH key to SSH agent:**
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

3. **Copy public key:**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

4. **Add to your Git hosting service:**
   - GitHub: Settings → SSH and GPG keys → New SSH key
   - GitLab: Preferences → SSH Keys
   - Bitbucket: Personal settings → SSH keys

### **Personal Access Token (Alternative)**

1. **GitHub:**
   - Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with `repo` scope

2. **GitLab:**
   - User Settings → Access Tokens
   - Create token with `read_repository` and `write_repository` scopes

3. **Bitbucket:**
   - Personal settings → App passwords
   - Create app password with repository permissions

## 📁 Repository Structure

Your repository will contain:

```
alrouf-quotation-microservice/
├── main.py                 # FastAPI application
├── test_main.py           # Unit tests
├── test_service.py        # Integration tests
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Local development
├── README.md             # Project documentation
├── env.example           # Environment template
├── .gitignore           # Git ignore rules
├── Makefile             # Development commands
└── quick_start.sh       # Startup script
```

## 🚀 Quick Commands

```bash
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to remote
git push origin main

# Pull latest changes
git pull origin main

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main
```

## 🔄 Workflow

### **Daily Development:**
1. `git pull origin main` - Get latest changes
2. Make your changes
3. `git add .` - Stage changes
4. `git commit -m "Description"` - Commit changes
5. `git push origin main` - Push to remote

### **Feature Development:**
1. `git checkout -b feature/feature-name`
2. Make changes and commit
3. `git push origin feature/feature-name`
4. Create Pull Request/Merge Request
5. Review and merge to main

## 📝 Commit Message Guidelines

Use clear, descriptive commit messages:

```bash
# Good examples:
git commit -m "Add quotation calculation logic"
git commit -m "Fix pricing calculation bug in margin calculation"
git commit -m "Update README with installation instructions"

# Avoid:
git commit -m "fix"
git commit -m "update"
git commit -m "stuff"
```

## 🆘 Troubleshooting

### **Authentication Issues:**
```bash
# Test SSH connection
ssh -T git@github.com

# Check remote URL
git remote -v

# Update remote URL if needed
git remote set-url origin git@github.com:USERNAME/REPOSITORY.git
```

### **Push Issues:**
```bash
# Force push (use with caution)
git push -f origin main

# Reset to remote state
git reset --hard origin/main
```

### **Merge Conflicts:**
```bash
# Abort merge
git merge --abort

# Reset to previous state
git reset --hard HEAD~1
```

## 📚 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [GitLab Documentation](https://docs.gitlab.com/)
- [Bitbucket Documentation](https://support.atlassian.com/bitbucket-cloud/)

## 🎯 Next Steps

After setting up your remote repository:

1. **Share the repository URL** with the Alrouf hiring team
2. **Create issues** for any bugs or feature requests
3. **Set up CI/CD** if needed (GitHub Actions, GitLab CI, etc.)
4. **Invite collaborators** if working with a team
5. **Set up project boards** for task management

---

**Need help?** Check the troubleshooting section above or refer to your Git hosting service's documentation.
