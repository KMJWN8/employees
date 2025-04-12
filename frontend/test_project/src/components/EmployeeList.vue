<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h3 v-if="localEmployees.length" class="text-xl font-bold text-gray-800">Список сотрудников</h3>
      <button

        @click="openAddEmployeeModal"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Добавить сотрудника
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Карточки сотрудников -->
      <EmployeeCard
        v-for="employee in localEmployees"
        :key="employee.id"
        :employee="employee"
        @delete-employee="deleteEmployee"
        @edit-employee="editEmployee"
      />
    </div>

    <div v-if="!localEmployees.length" class="text-center text-gray-500">
      <p class="mt-5">Нет сотрудников в этом подразделении.</p>
    </div>

    <!-- Модальное окно для добавления сотрудника -->
    <div v-if="isModalOpen" class="fixed inset-0 bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-lg w-[400px]">
        <h2 class="text-xl font-bold mb-4">Добавить сотрудника</h2>
        <form @submit.prevent="addEmployee">
          <div class="mb-4">
            <label class="block text-gray-700">ФИО</label>
            <input
              v-model="newEmployee.full_name"
              type="text"
              class="w-full border border-gray-300 rounded px-3 py-2"
              required
            />
          </div>
          <div class="mb-4">
            <label class="block text-gray-700">Должность</label>
            <input
              v-model="newEmployee.position"
              type="text"
              class="w-full border border-gray-300 rounded px-3 py-2"
              required
            />
          </div>
          <div class="mb-4">
            <label class="block text-gray-700">Фото сотрудника</label>
            <input
              type="file"
              @change="photoUpload"
              class="w-full border border-gray-300 rounded px-3 py-2"
              required
            />
          </div>
          <div class="mb-4">
            <label class="block text-gray-700">Дата рождения</label>
            <input
              v-model="newEmployee.date_of_birth"
              type="date"
              class="w-full border border-gray-300 rounded px-3 py-2"
              required
            />
          </div>
          <div class="mb-4">
            <label class="block text-gray-700">Дата начала работы</label>
            <input
              v-model="newEmployee.start_date"
              type="date"
              class="w-full border border-gray-300 rounded px-3 py-2"
              required
            />
          </div>
          <div class="mb-4">
            <label class="block text-gray-700">Группа</label>
            <select
              v-model="newEmployee.team"
              class="w-full border border-gray-300 rounded px-3 py-2"
              required
            >
              <option v-for="team in availableTeams" :key="team.id" :value="team.id">
                {{ team.name }}
              </option>
            </select>
          </div>
          <div class="flex justify-end">
            <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
              Сохранить
            </button>
            <button
              @click="closeModal"
              class="ml-2 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
            >
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>
 
    <!-- Модальное окно для редактирования сотрудника -->
  <div v-if="isEditModalOpen" class="fixed inset-0 bg-opacity-50 flex items-center justify-center">
  <div class="bg-white p-6 rounded-lg shadow-lg w-[400px]">
    <h2 class="text-xl font-bold mb-4">Редактировать сотрудника</h2>
    <form @submit.prevent="saveEditedEmployee">
      <div class="mb-4">
        <label class="block text-gray-700">ФИО</label>
        <input
          v-model="editedEmployee.full_name"
          type="text"
          class="w-full border border-gray-300 rounded px-3 py-2"
          required
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700">Должность</label>
        <input
          v-model="editedEmployee.position"
          type="text"
          class="w-full border border-gray-300 rounded px-3 py-2"
          required
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700">Дата рождения</label>
        <input
          v-model="editedEmployee.date_of_birth"
          type="date"
          class="w-full border border-gray-300 rounded px-3 py-2"
          required
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700">Дата начала работы</label>
        <input
          v-model="editedEmployee.start_date"
          type="date"
          class="w-full border border-gray-300 rounded px-3 py-2"
          required
        />
      </div>
      <div class="flex justify-end">
        <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
          Сохранить
        </button>
        <button
          @click="closeEditModal"
          class="ml-2 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
        >
          Отмена
        </button>
      </div>
    </form>
  </div>
</div>
</div>
</template>

<script setup>
import { ref, computed, watch} from 'vue'
import axios from 'axios'
import EmployeeCard from './EmployeeCard.vue'

const props = defineProps({
  employees: {
    type: Array,
    required: true,
  },
  selectedNode: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['refresh-employees', 'delete-employee'])

const isModalOpen = ref(false)

const newEmployee = ref({
  full_name: '',
  position: '',
  date_of_birth: '',
  start_date: '',
  team: null,
  photo: null,
})

const photoUpload = (event) => {
  const file = event.target.files[0]
  newEmployee.value.photo = file
}

// Вычисляем доступные группы для выбора
const availableTeams = computed(() => {
  if (!props.selectedNode) return []

  const teams = []
  function collectTeams(node) {
    if (node.type === 'team') {
      teams.push({ id: node.id, name: node.label })
    }
    if (node.children) {
      node.children.forEach(child => collectTeams(child))
    }
  }

  collectTeams(props.selectedNode)
  return teams
})

const openAddEmployeeModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  resetForm()
}

const resetForm = () => {
  newEmployee.value = {
    full_name: '',
    position: '',
    date_of_birth: '',
    start_date: '',
    team: null,
    photo: null,
  }
}

// Создаем локальную копию массива
const localEmployees = ref([...props.employees])

// Наблюдаем за изменениями props.employees
watch(
  () => props.employees,
  (newEmployees) => {
    localEmployees.value = [...newEmployees]
  }
)

const addEmployee = async () => {
  const formData = new FormData();
  formData.append('full_name', newEmployee.value.full_name);
  formData.append('position', newEmployee.value.position);
  formData.append('date_of_birth', newEmployee.value.date_of_birth);
  formData.append('start_date', newEmployee.value.start_date);
  formData.append('team', newEmployee.value.team);

  if (newEmployee.value.photo) {
    formData.append('photo', newEmployee.value.photo); // Добавляем файл в FormData
  }

  const response = await axios.post('http://127.0.0.1:8000/api/employees/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

  console.log('Сотрудник добавлен:', response.data);

  const employeeId = response.data.id // Получаем ID созданного сотрудника

  // Шаг 2: Добавляем сотрудника в выбранную группу через PATCH
  const teamId = newEmployee.value.team
  await axios.patch(`http://127.0.0.1:8000/api/teams/${teamId}/add-member/`, {
    member_id: employeeId,
  })
  // Добавляем сотрудника в локальный список
  localEmployees.value.push(response.data)

  // Закрыть модальное окно и очистить форму
  closeModal()

  // Обновить список сотрудников
  emit('refresh-employees')
}

const deleteEmployee = (employeeId) => {
  // Удаляем сотрудника из локального массива
  localEmployees.value = localEmployees.value.filter(emp => emp.id !== employeeId)
  emit('refresh-employees')
}

const isEditModalOpen = ref(false)
const editedEmployee = ref(null)

const editEmployee = (employee) => {
  editedEmployee.value = { ...employee } // Создаем копию сотрудника
  isEditModalOpen.value = true
}

const closeEditModal = () => {
  isEditModalOpen.value = false
  editedEmployee.value = null
}

const saveEditedEmployee = async () => {
  try {
    await axios.put(`http://127.0.0.1:8000/api/employees/${editedEmployee.value.id}/`, editedEmployee.value, photo = null)
    // Обновляем локальный массив
    const index = localEmployees.value.findIndex(emp => emp.id === editedEmployee.value.id)
    if (index !== -1) {
      localEmployees.value[index] = { ...editedEmployee.value }
    }
    closeEditModal()
  } catch (error) {
    console.error('Ошибка при редактировании сотрудника:', error.response?.data)
  }
}
</script>