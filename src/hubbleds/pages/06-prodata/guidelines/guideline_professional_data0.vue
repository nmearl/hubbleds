<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    header-text="Professional Data"
    :allow-back="false"
    @next="next_callback()"
    :can-advance="can_advance"
  >
  
    <template #back-content>
      <div>
        Open menu to return to earlier stages.<br>
        (Open/close menu with <v-btn icon tile dark x-small disabled class="mx-1" elevation="2" style="background-color: #172c4d; border-radius: 5px;"><v-icon style="color:white!important;">mdi-menu</v-icon></v-btn> above)
      </div>
    </template>
    <div
      class="mb-4"
    >
      Let's now turn to professional astronomers' data and see how that compares to your class's data.
    </div>
  </scaffold-alert>
</template>

<script setup>
</script>


