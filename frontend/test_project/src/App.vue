<template>
  <div class="common-layout">
    <el-container class="flex flex-col">
      <el-header class="bg-[#161F6D] shadow-md flex flex-row">
        <img src="@/assets/icons/icon.png" class="w-10 h-10 ml-8 my-2" />
        <div class="my-3 mx-8 text-2xl font-bold text-amber-50">
            ГИС учета сотрудников
        </div>
        <input
          class="bg-white my-4 rounded-md pr-2 pl-2 "
          placeholder="Поиск"
          type="text"
          v-model="searchQuery"
          @input="searchEmployees"
        />
      </el-header>
      <el-container class="flex-1">
        <el-aside class="shadow-md">
          <Tree 
          :tree-data="treeData" 
          @node-selected="onNodeSelected" 
          @refresh-tree="fetchData"
          />
        </el-aside>
        <el-main>
          <Statistics v-if="selectedEmployees.length" :statistics="currentStatistics" />
            <EmployeeList 
            :employees="selectedEmployees"
            :selected-node="selectedNode"
            @refresh-employees="fetchData" 
            />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

import Tree from './components/Tree.vue'
import EmployeeList from './components/EmployeeList.vue'
import Statistics from './components/Statistics.vue'


const treeData = ref([])

const transformData = (apiData) => {
  return apiData.map((service) => ({
    id: service.id,
    label: service.name,
    type: 'service',
    children: service.departments.map((department) => ({
      id: department.id,
      label: department.name,
      type: 'department',
      children: department.divisions.map((division) => ({
        id: division.id,
        label: division.name,
        type: 'division',
        children: division.teams.map((team) => ({
          id: team.id,
          label: team.name,
          type: 'team',
          members: team.members,
        })),
      })),
    })),
  }))
}

const base_url = 'http://127.0.0.1:8000/api/'

const fetchData = async (expandedKeys = []) => {
  const response = await axios.get(`${base_url}services/`)
  treeData.value = transformData(response.data)
  expandedKeys.forEach(key => expandedKeys.value.push(key))
}

const selectedNode = ref(null)
const selectedEmployees = ref([])
const currentStatistics = ref(null)

const onNodeSelected = async (node) => {
  selectedNode.value = node
  selectedEmployees.value = collectEmployees(node)

  let url = ''
    // Формируем URL в зависимости от типа узла
  switch (node.type) {
    case 'service':
      url = `${base_url}services/${node.id}/statistics/`
      break
    case 'department':
      url = `${base_url}departments/${node.id}/statistics/`
      break
    case 'division':
      url = `${base_url}divisions/${node.id}/statistics/`
      break
    case 'team':
      url = `${base_url}teams/${node.id}/statistics/`
      break
    default:
      console.error('Неизвестный тип узла:', node.type)
      return
  }

  const response = await axios.get(url)
  currentStatistics.value = response.data
}


// Рекурсивный сбор сотрудников
const collectEmployees = (node) => {
  const employees = []

  function recurse(currentNode) {
    if (currentNode.members) {
        currentNode.members.forEach(member => employees.push(member))
    }

    if (currentNode.children) {
        currentNode.children.forEach(child => recurse(child))
    }
  }

  recurse(node)
  return employees
}

const searchQuery = ref('')

const searchEmployees = async () => {
  const response = await axios.get(`${base_url}employees/?search=${searchQuery.value}`)
  selectedEmployees.value = response.data
}

// Вызов функции загрузки данных при инициализации
fetchData()

</script>

<style>

.el-aside{
  width: fit-content !important;
  transition: width 0.3s ease-in-out !important;
}
.scrollable-content {
  overflow-y: auto; /* Добавляем прокрутку по вертикали */
  height: 100vh;
  overscroll-behavior: contain;
}
.el-main{
  padding-top: 5px !important;
}
.el-container{
  overflow: hidden;
}

</style>