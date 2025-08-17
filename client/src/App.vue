<script setup>
import { RouterView } from 'vue-router'
import { useHeaderContent } from '@/composables/useHeaderContent'
import HeaderTitle from '@/components/common/HeaderTitle.vue'
import Navbar from '@/components/layouts/Navbar.vue'
import Footer from '@/components/layouts/Footer.vue'

const { headerContent } = useHeaderContent()
</script>

<template>
  <header>
    <Navbar />
    <HeaderTitle v-if="headerContent.content" class="px-4 sm:px-6 md:px-8">
      {{ headerContent.content }}
    </HeaderTitle>
  </header>

  <main class="flex flex-col flex-1 container font-medium mx-auto px-4 sm:px-6 md:px-8">
    <RouterView />
  </main>

  <Footer />
</template>
