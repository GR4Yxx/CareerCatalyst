<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1 class="title">404</h1>
      <h2 class="subtitle">Page Not Found</h2>
      <p class="description">The page you are looking for doesn't exist or has been moved.</p>
      <router-link to="/" class="back-button"> Go to Home </router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
  padding: 40px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 8rem;
  font-weight: bold;
  color: #4f46e5;
  margin: 0;
  line-height: 1;
}

.subtitle {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
  margin: 10px 0 20px;
}

.description {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 30px;
}

.back-button {
  display: inline-block;
  padding: 12px 24px;
  background-color: #4f46e5;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #4338ca;
}
</style>
