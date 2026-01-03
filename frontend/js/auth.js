// Authentication handling for Mój Portfel 2026

// Toast notification function
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span>${message}</span>
  `;
  container.appendChild(toast);
  
  // Auto dismiss after 4 seconds
  setTimeout(() => {
    toast.style.animation = 'fadeOut 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Login page
if (window.location.pathname.includes('login.html')) {
  const loginForm = document.getElementById('loginForm');
  const loginBtn = document.getElementById('loginBtn');
  const errorMessage = document.getElementById('errorMessage');
  
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Show loading state
    loginBtn.disabled = true;
    loginBtn.querySelector('span').textContent = 'Logowanie...';
    loginBtn.querySelector('.spinner').classList.remove('hidden');
    errorMessage.classList.add('hidden');
    
    try {
      await API.login(email, password);
      showToast('Zalogowano pomyślnie!', 'success');
      
      // Redirect to dashboard
      setTimeout(() => {
        window.location.href = '/index.html';
      }, 500);
    } catch (error) {
      errorMessage.textContent = error.message || 'Błąd logowania. Sprawdź dane i spróbuj ponownie.';
      errorMessage.classList.remove('hidden');
      
      // Shake animation
      loginForm.style.animation = 'shake 0.5s';
      setTimeout(() => loginForm.style.animation = '', 500);
      
      showToast(error.message, 'error');
    } finally {
      loginBtn.disabled = false;
      loginBtn.querySelector('span').textContent = 'Zaloguj się';
      loginBtn.querySelector('.spinner').classList.add('hidden');
    }
  });
}

// Register page
if (window.location.pathname.includes('register.html')) {
  const registerForm = document.getElementById('registerForm');
  const registerBtn = document.getElementById('registerBtn');
  const errorMessage = document.getElementById('errorMessage');
  
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // Validate passwords match
    if (password !== confirmPassword) {
      errorMessage.textContent = 'Hasła nie są identyczne';
      errorMessage.classList.remove('hidden');
      showToast('Hasła nie są identyczne', 'error');
      return;
    }
    
    // Show loading state
    registerBtn.disabled = true;
    registerBtn.querySelector('span').textContent = 'Rejestrowanie...';
    registerBtn.querySelector('.spinner').classList.remove('hidden');
    errorMessage.classList.add('hidden');
    
    try {
      await API.register(email, password);
      showToast('Konto utworzone pomyślnie!', 'success');
      
      // Redirect to dashboard
      setTimeout(() => {
        window.location.href = '/index.html';
      }, 500);
    } catch (error) {
      errorMessage.textContent = error.message || 'Błąd rejestracji. Spróbuj ponownie.';
      errorMessage.classList.remove('hidden');
      
      // Shake animation
      registerForm.style.animation = 'shake 0.5s';
      setTimeout(() => registerForm.style.animation = '', 500);
      
      showToast(error.message, 'error');
    } finally {
      registerBtn.disabled = false;
      registerBtn.querySelector('span').textContent = 'Zarejestruj się';
      registerBtn.querySelector('.spinner').classList.add('hidden');
    }
  });
  
  // Password strength indicator
  const passwordInput = document.getElementById('password');
  passwordInput.addEventListener('input', (e) => {
    const password = e.target.value;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasMinLength = password.length >= 8;
    
    if (hasUpperCase && hasLowerCase && hasNumber && hasMinLength) {
      passwordInput.classList.remove('input-error');
      passwordInput.classList.add('input-success');
    } else {
      passwordInput.classList.remove('input-success');
      if (password.length > 0) {
        passwordInput.classList.add('input-error');
      }
    }
  });
}

// Check if user is authenticated on protected pages
if (!window.location.pathname.includes('login.html') && !window.location.pathname.includes('register.html')) {
  const token = localStorage.getItem('accessToken');
  if (!token) {
    window.location.href = '/login.html';
  }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { showToast };
}
