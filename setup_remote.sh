#!/bin/bash

echo "🚀 Alrouf Quotation Microservice - Remote Repository Setup"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_error "Git repository not initialized. Run 'git init' first."
    exit 1
fi

# Check if we have commits
if ! git rev-parse HEAD >/dev/null 2>&1; then
    print_error "No commits found. Make your first commit before setting up remote."
    exit 1
fi

echo ""
print_info "Choose your Git hosting service:"
echo "1) GitHub"
echo "2) GitLab"
echo "3) Bitbucket"
echo "4) Custom/Other"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        SERVICE="GitHub"
        BASE_URL="https://github.com"
        SSH_URL="git@github.com"
        ;;
    2)
        SERVICE="GitLab"
        BASE_URL="https://gitlab.com"
        SSH_URL="git@gitlab.com"
        ;;
    3)
        SERVICE="Bitbucket"
        BASE_URL="https://bitbucket.org"
        SSH_URL="git@bitbucket.org"
        ;;
    4)
        SERVICE="Custom"
        BASE_URL=""
        SSH_URL=""
        ;;
    *)
        print_error "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
print_info "Repository setup for $SERVICE"

if [ "$SERVICE" != "Custom" ]; then
    echo ""
    print_info "Please create a new repository on $SERVICE:"
    echo "1. Go to $BASE_URL"
    echo "2. Create new repository"
    echo "3. Repository name: alrouf-quotation-microservice"
    echo "4. Description: FastAPI-based quotation microservice for Alrouf Lighting Technology evaluation task"
    echo "5. Choose visibility (Public/Private)"
    echo "6. DO NOT initialize with README, .gitignore, or license (we already have files)"
    echo ""
    
    read -p "Press Enter when you've created the repository..."
fi

echo ""
print_info "Enter your $SERVICE username:"
read -p "Username: " username

if [ "$SERVICE" != "Custom" ]; then
    REPO_NAME="alrouf-quotation-microservice"
    HTTPS_URL="$BASE_URL/$username/$REPO_NAME.git"
    SSH_URL_FULL="$SSH_URL:$username/$REPO_NAME.git"
else
    echo ""
    print_info "Enter your custom repository URL:"
    read -p "Repository URL: " HTTPS_URL
    SSH_URL_FULL=""
fi

echo ""
print_info "Choose authentication method:"
echo "1) HTTPS (Personal Access Token)"
echo "2) SSH (SSH Key)"
echo ""

read -p "Enter your choice (1-2): " auth_choice

case $auth_choice in
    1)
        print_info "Using HTTPS authentication"
        REMOTE_URL="$HTTPS_URL"
        print_warning "Make sure you have a Personal Access Token configured"
        ;;
    2)
        print_info "Using SSH authentication"
        if [ "$SERVICE" != "Custom" ]; then
            REMOTE_URL="$SSH_URL_FULL"
            print_warning "Make sure you have SSH keys configured"
        else
            print_error "SSH not supported for custom repositories in this script"
            print_info "Please add the remote manually: git remote add origin <your-url>"
            exit 1
        fi
        ;;
    *)
        print_error "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
print_info "Adding remote origin..."
if git remote add origin "$REMOTE_URL"; then
    print_status "Remote origin added successfully"
else
    print_error "Failed to add remote origin"
    print_info "You may need to remove existing remote first: git remote remove origin"
    exit 1
fi

echo ""
print_info "Verifying remote configuration..."
git remote -v

echo ""
print_info "Pushing to remote repository..."
if git push -u origin main; then
    print_status "Successfully pushed to remote repository!"
    echo ""
    print_info "Your repository is now available at:"
    if [ "$SERVICE" != "Custom" ]; then
        echo "$BASE_URL/$username/$REPO_NAME"
    else
        echo "$HTTPS_URL"
    fi
    echo ""
    print_info "Next steps:"
    echo "1. Share the repository URL with the Alrouf hiring team"
    echo "2. Set up branch protection rules (recommended)"
    echo "3. Configure CI/CD if needed"
    echo "4. Invite collaborators if working with a team"
else
    print_error "Failed to push to remote repository"
    echo ""
    print_info "Common issues and solutions:"
    echo "1. Authentication failed: Check your credentials/SSH keys"
    echo "2. Repository not found: Verify the repository exists and you have access"
    echo "3. Permission denied: Check your account permissions"
    echo ""
    print_info "You can try again with: git push -u origin main"
fi

echo ""
print_info "Setup complete! Check REPOSITORY_SETUP.md for detailed instructions."
