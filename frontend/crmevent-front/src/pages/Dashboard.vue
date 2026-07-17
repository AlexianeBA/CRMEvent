<template>

<DashboardLayout>

<div class="grid">

<div class="left">

<NextEventCard/>

<StatsCard/>

<StatsCard/>

</div>

<div class="center">

<UpcomingEvents/>

<TimelineCard/>

</div>

<div class="right">

<ProvidersCard/>

<TasksCard/>

</div>

</div>

</DashboardLayout>

</template>

<script setup>
import DashboardLayout from "@/layouts/DashboardLayout.vue"

import NextEventCard from "@/components/dashboard/NextEventCard.vue"
import StatsCard from "@/components/dashboard/StatsCard.vue"
import UpcomingEvents from "@/components/dashboard/UpcomingEvents.vue"
import TimelineCard from "@/components/dashboard/TimelineCard.vue"
import ProvidersCard from "@/components/dashboard/ProvidersCard.vue"
import TasksCard from "@/components/dashboard/TasksCard.vue"
</script>

<style scoped>

.grid{

display:grid;

grid-template-columns:280px 1fr 330px;

gap:25px;

}

.left,

.center,

.right{

display:flex;

flex-direction:column;

gap:25px;

}

</style>