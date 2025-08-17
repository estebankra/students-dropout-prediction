<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminUsersStore } from '@/stores/admin/users'
import { useHeaderContent } from '@/composables/useHeaderContent'
import AdminUsersForm from '@/components/admin/users/Form.vue'
import AdminUsersFilters from '@/components/admin/users/Filters.vue'
import AdminUsersList from '@/components/admin/users/List.vue'
import LoadMore from '@/components/common/LoadMore.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import NoResultsFound from '@/components/common/NoResultsFound.vue'

const isLoading = ref(false)
const userToEdit = ref(null)
const { setHeaderContent } = useHeaderContent()
const adminUsersStore = useAdminUsersStore()
const users = computed(() => adminUsersStore.getUsers)

const cancelEditUser = () => {
  userToEdit.value = null
}

const handleEditUser = (user) => {
  userToEdit.value = user
}

const fetchData = async (userFilters = null) => {
  if (userFilters) adminUsersStore.resetUsersState()
  const newOffset = users.value.offset + users.value.limit
  if (newOffset > users.value.total) return

  isLoading.value = true
  adminUsersStore
    .fetchUsers({
      filters: userFilters,
      offset: newOffset,
      limit: 25
    })
    .finally(() => {
      isLoading.value = false
    })
}

onMounted(() => {
  setHeaderContent('Usuarios')
  adminUsersStore.resetUsersState()
  fetchData()
})
</script>

<template>
  <section class="flex flex-col">
    <div class="flex justify-end items-center gap-6">
      <AdminUsersFilters @filtersUpdated="fetchData" />
      <AdminUsersForm :userToEdit="userToEdit" @cancelEditUser="cancelEditUser" />
    </div>
    <section v-if="users.items.length">
      <AdminUsersList :users="users.items" @editUser="handleEditUser" />
      <LoadMore v-if="users.offset + users.limit < users.total" @loadMore="fetchData" />
    </section>
    <NoResultsFound v-else-if="!isLoading" />
    <LoadingState v-if="isLoading" />
  </section>
</template>
