<template>
  <div class="flex gap-4 p-4 bg-white border border-slate-100 rounded-lg shadow-2xs hover:-translate-y-1 hover:shadow-md transition">
    <div class="flex-shrink-0 w-24 h-24 rounded-full overflow-hidden bg-gray-200 flex items-center justify-center">
      <img
        v-if="employee.photo"
        :src="getPhotoUrl(employee.photo)"
        class="w-full h-full object-cover"
      />
      <span v-else class="text-sm text-gray-500">Нет фото</span>
    </div>
    <div class="flex-grow">
      <h3 class="text-lg font-bold">{{ employee.full_name }}</h3>
      <p class="text-sm text-gray-600"><strong>Должность:</strong> {{ employee.position }}</p>
      <p class="text-sm text-gray-600"><strong>Дата рождения:</strong> {{ formatDate(employee.date_of_birth) }}</p>
      <p class="text-sm text-gray-600"><strong>Дата начала работы:</strong> {{ formatDate(employee.start_date) }}</p>
      <p class="text-sm text-gray-600"><strong>Место работы:</strong> {{ employee.team }}</p>
    </div>
    <div class="flex flex-col gap-2">
      <!-- Кнопка редактирования -->
      <img
        @click="editEmployee"
        src="@/assets/icons/edit_icon.png"
        alt="Редактировать"
        class="cursor-pointer hover:opacity-75 transition-opacity rounded-md w-5 h-5"
      />
      <!-- Кнопка удаления -->
      <img
        @click="deleteEmployee"
        src="@/assets/icons/delete_icon.png"
        alt="Удалить"
        class="cursor-pointer hover:opacity-75 transition-opacity rounded-md w-5 h-5"
      />

    </div>
  </div>
</template>

<script setup>
import axios from 'axios'

const props = defineProps({
  employee: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['delete-employee', 'edit-employee'])

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

const getPhotoUrl = (photoPath) => {
  if (!photoPath) return null
  return photoPath.startsWith('http') ? photoPath : `http://127.0.0.1:8000${photoPath}`
}

const deleteEmployee = async () => {
  await axios.delete(`http://127.0.0.1:8000/api/employees/${props.employee.id}/`)
  emit('delete-employee', props.employee.id) // Уведомляем родителя об удалении
}

const editEmployee = () => {
  emit('edit-employee', props.employee) // Уведомляем родителя о редактировании
}
</script>
