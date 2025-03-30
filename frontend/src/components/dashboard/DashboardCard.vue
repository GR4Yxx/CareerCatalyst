<template>
  <div class="bg-card rounded-lg shadow p-4 border">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="font-medium text-muted-foreground">{{ title }}</h3>
        <p class="text-3xl font-bold mt-1">
          <span v-if="loading">
            <span class="animate-pulse">...</span>
          </span>
          <span v-else>{{ count }}</span>
        </p>
      </div>
      <div class="text-primary">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  title: {
    type: String,
    required: true,
  },
  count: {
    type: Number,
    default: 0,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})
</script>
