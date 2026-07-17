<template>
  <div class="layout">

    <Sidebar />

    <div class="content">

      <Header />

      <slot />

    </div>

  </div>
</template>

<script setup>
import Sidebar from "@/layouts/Sidebar.vue"
import Header from "@/components/dashboard/Header.vue"
</script>

<style scoped>

.layout{
    display:flex;
    min-height:100vh;
    background:#f6f8fc;
}

.content{
    flex:1;
    padding:30px;
}

</style>