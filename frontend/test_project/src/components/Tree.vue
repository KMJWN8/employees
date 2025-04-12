<template>
  <div class="relative">
    <div class="font-bold m-2 text-center text-xl border-b-gray-500 text-gray-800">
      Список подразделений
    </div>
    <el-tree
      class="pl-3 pr-3"
      :data="treeData"
      node-key="id"
      :default-expanded-keys="expandedKeys"
      @node-click="nodeClick"
      @node-expand="nodeExpand"
      @node-contextmenu="rightClick"
    />

    <!-- Контекстное меню -->
  <div 
    v-if="contextMenu.visible" 
    class="fixed bg-white border border-gray-300 rounded-lg shadow-lg py-2 w-70 z-50"
    :style="{ top: contextMenu.y + 'px', left: contextMenu.x + 'px' }">
      <div 
      v-if="selectedNode?.type !== 'team'"
        class="px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900 cursor-pointer transition"
        @click="openForm('add')">
        ➕ Добавить дочерний узел
      </div>
      <div 
        class="px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900 cursor-pointer transition"
        @click="openForm('edit')">
        ✏️ Редактировать узел
      </div>
      <div 
        class="px-4 py-2 text-red-600 hover:bg-red-100 hover:text-red-800 cursor-pointer transition"
        @click="deleteNode">
        🗑️ Удалить узел
      </div>
  </div>

    <!-- Модальное окно с формой -->
    <el-dialog
      v-model="formDialogVisible"
      :title="formTitle"
      width="400px"
      @close="resetForm"
    >
      <el-form :model="form" ref="formRef" label-position="top">
        <el-form-item label="Имя узла" prop="name">
          <el-input v-model="form.name" placeholder="Введите имя узла"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">Сохранить</el-button>
          <el-button @click="formDialogVisible = false">Отмена</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

defineProps({
  treeData: Array,
})

const emit = defineEmits(['node-selected', 'refresh-tree'])

const expandedKeys = ref([])
const selectedNode = ref(null)
const contextMenu = ref({ visible: false, x: 0, y: 0 })

const formDialogVisible = ref(false)
const formTitle = ref('')
const formMode = ref('') // 'add' или 'edit'
const form = ref({name: '',})

const nodeClick = (node) => {
  emit('node-selected', node)
}

const nodeExpand = (node) => {
  expandedKeys.value.push(node.id)
}

const rightClick = (event, node) => {
  selectedNode.value = node
  contextMenu.value = { visible: true, x: event.clientX, y: event.clientY }
}

const openForm = (mode) => {
  formMode.value = mode;
  formTitle.value = mode === 'add' ? 'Добавить дочерний узел' : 'Редактировать узел'
  form.value.name = mode === 'edit' ? selectedNode.value.label : ''
  formDialogVisible.value = true
  contextMenu.value.visible = false
};

const submitForm = async () => {
  if (formMode.value === 'add') {
    let parentKey = ''
    let childKey = ''
    switch (selectedNode.value.type) {
      case 'service':
        parentKey = 'service'
        childKey = 'department'
        break;
      case 'department':
        parentKey = 'department'
        childKey = 'division'
        break;
      case 'division':
        parentKey = 'division'
        childKey = 'team'
        break;
      default:
        console.log('Неизвестный тип узла')
        return;
    }

    const url = `http://127.0.0.1:8000/api/${childKey}s/`
    await axios.post(url, { name: form.value.name, [parentKey]: selectedNode.value.id })
  } 
  else if (formMode.value === 'edit') {
    const url = `http://127.0.0.1:8000/api/${selectedNode.value.type}s/${selectedNode.value.id}/`
    await axios.patch(url, { name: form.value.name })
  }
  
  emit('refresh-tree', expandedKeys.value)
    formDialogVisible.value = false
  };
  
  const deleteNode = async () => {
  if (!selectedNode.value) return
    const url = `http://127.0.0.1:8000/api/${selectedNode.value.type}s/${selectedNode.value.id}/`
    await axios.delete(url)
    emit('refresh-tree', expandedKeys.value)
    contextMenu.value.visible = false
  }
  
  const resetForm = () => {
    form.value.name = ''
  }
  
  onMounted(() => {
    document.addEventListener('click', () => {
    contextMenu.value.visible = false
    })
  })

</script>
<style>
  .el-tree-node__content{
      color: black !important;
  }

  .el-tree-node__expand-icon {
    color: black !important;
  }

  .el-tree {
    --el-tree-node-hover-bg-color: #00ABE1 !important;
  }

  .el-button--primary {
    --el-button-bg-color: #161F6D !important; 
  }
</style>