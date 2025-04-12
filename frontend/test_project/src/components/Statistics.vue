<template>
  <div v-if="statistics" class="p-4 bg-white rounded-lg shadow-2xs border border-gray-200 my-2">
    <h3 class="text-xl font-semibold text-gray-800 mb-3 flex items-center">
      <img src="@/assets/icons/bar_chart.png" alt="Статистика" class="w-6 h-6 mr-2" />
      Статистика подразделения
    </h3>
    <ul class="divide-y divide-gray-200">
      <li class="py-1 flex items-center">
        <img src="@/assets/icons/people.png" alt="Количество сотрудников" class="w-5 h-5 mr-3" />
        <strong class="text-gray-700">Количество сотрудников:</strong>
        <span class="ml-auto text-gray-900 font-medium">{{ statistics.employee_count }}</span>
      </li>
      <li class="py-1 flex items-center">
        <img src="@/assets/icons/cake.png" alt="Средний возраст" class="w-5 h-5 mr-3" />
        <strong class="text-gray-700">Средний возраст:</strong>
        <span class="ml-auto text-gray-900 font-medium">{{ statistics.average_age }} {{ getPlural(statistics.average_age, ['год', 'года', 'лет']) }}</span>
      </li>
      <li class="py-1 flex items-center">
        <img src="@/assets/icons/work.png" alt="Средний стаж" class="w-5 h-5 mr-3" />
        <strong class="text-gray-700">Средний стаж:</strong>
        <span class="ml-auto text-gray-900 font-medium">{{ statistics.average_tenure }} {{ getPlural(statistics.average_tenure, ['год', 'года', 'лет']) }}</span>
      </li>
    </ul>
  </div>

  <div v-else class="p-6 bg-white rounded-lg shadow-lg border border-gray-200">
    <p class="text-gray-600 text-center flex items-center justify-center">
      <img src="@/assets/icons/info.png" alt="Информация" class="w-5 h-5 mr-2" />
      Выберите подразделение для просмотра статистики.
    </p>
  </div>
</template>

<script setup>

defineProps({
  statistics: {
    type: Object,
    default: null,
  },
})

/* Функция, которая позволяет учитывать особенности русского языка 
при использовании слов "год" и "лет"*/
function getPlural(number, words) {
  const cases = [2, 0, 1, 1, 1, 2]
  return words[
    (number % 100 > 4 && number % 100 < 20) 
      ? 2 
      : cases[Math.min(number % 10, 5)]
  ]
}
</script>