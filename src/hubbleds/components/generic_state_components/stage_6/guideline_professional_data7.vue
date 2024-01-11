<!-- # multiple choice -->
<template>
  <guideline-professional-data
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    prev-marker="pro_dat6"
    next-marker="pro_dat8"
    v-slot:default="{ advance, allowAdvancing }"
    :state="state"
    :index="7"
  >
    <div
      class="mb-4"
    >
      Whose age estimate are you more inclined to believe?
      <v-container
        class="px-0"
        fluid
      >
        <mc-radiogroup
          :radio-options="['Our age estimate', 'Hubble team\'s age estimate']"
          :feedbacks="['Interesting! Why do you choose that?','Interesting! Why do you choose that?']"
          :correct-answers="[]"
          :neutral-answers='[0,1]'
          @select="(status) => { if (status.neutral) { allowAdvancing(); } }"
          score-tag="pro-dat7"
        >
        </mc-radiogroup>
      </v-container>
      <free-response
        outlined
        auto-grow
        rows=2
        label="Why?"
        tag="prodata-free-7"
        v-if="advance"
      ></free-response>
    </div>
  </guideline-professional-data>
</template>

<script>
module.exports = {
 props: ['state']
}
</script>
