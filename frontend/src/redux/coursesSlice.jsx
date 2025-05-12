// src/redux/coursesSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import apiService from './apiService';
import { logoutUser } from './authSlice';

// Async thunk for fetching user's courses
// Async thunk for fetching user's courses (list view)
export const fetchUserCourses = createAsyncThunk(
  'courses/fetchUserCourses',
  async (_, { getState, rejectWithValue }) => {
    const { auth } = getState();
    if (!auth.isAuthenticated) {
      return rejectWithValue('User not authenticated');
    }
    try {
      const response = await apiService.get('/courses');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || error.message || 'Failed to fetch courses');
    }
  }
);

export const createNewCourse = createAsyncThunk(
  'courses/createNewCourse',
  async (courseData, { rejectWithValue }) => {
    try {
      const response = await apiService.post('/courses', courseData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || error.message || 'Failed to create course');
    }
  }
);

export const fetchCourseById = createAsyncThunk(
  'courses/fetchCourseById',
  async (courseId, { getState, rejectWithValue }) => {
    const { auth } = getState();
    if (!auth.isAuthenticated) {
      return rejectWithValue('User not authenticated to view course details');
    }
    try {
      const response = await apiService.get(`/courses/${courseId}`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || error.message || 'Failed to fetch course details');
    }
  }
);

// --- Initial State ---
const initialState = {
  items: [],
  selectedCourse: null,
  loading: 'idle',
  selectedCourseLoading: 'idle',
  error: null,
  selectedCourseError: null,
};

// --- Slice Definition ---
const coursesSlice = createSlice({
  name: 'courses',
  initialState,
  reducers: {
    clearCoursesError: (state) => {
      state.error = null;
    },
    clearSelectedCourseError: (state) => {
      state.selectedCourseError = null;
    },
    clearSelectedCourse: (state) => {
      state.selectedCourse = null;
      state.selectedCourseError = null;
      state.selectedCourseLoading = 'idle';
    },
    // Optional: A specific action to clear all course data if needed outside of logout
    resetCoursesState: () => initialState,
  },
  extraReducers: (builder) => {
    builder
      // fetchUserCourses
      .addCase(fetchUserCourses.pending, (state) => {
        state.loading = 'pending';
        state.error = null;
      })
      .addCase(fetchUserCourses.fulfilled, (state, action) => {
        state.loading = 'succeeded';
        state.items = action.payload || [];
      })
      .addCase(fetchUserCourses.rejected, (state, action) => {
        state.loading = 'failed';
        state.items = [];
        state.error = action.payload;
      })

      // createNewCourse
      .addCase(createNewCourse.pending, (state) => {
        state.loading = 'pending';
        state.error = null;
      })
      .addCase(createNewCourse.fulfilled, (state, action) => {
        state.loading = 'succeeded';
        state.items.push(action.payload);
      })
      .addCase(createNewCourse.rejected, (state, action) => {
        state.loading = 'failed';
        state.error = action.payload;
      })

      // fetchCourseById
      .addCase(fetchCourseById.pending, (state) => {
        state.selectedCourseLoading = 'pending';
        state.selectedCourse = null;
        state.selectedCourseError = null;
      })
      .addCase(fetchCourseById.fulfilled, (state, action) => {
        state.selectedCourseLoading = 'succeeded';
        state.selectedCourse = action.payload;
      })
      .addCase(fetchCourseById.rejected, (state, action) => {
        state.selectedCourseLoading = 'failed';
        state.selectedCourse = null;
        state.selectedCourseError = action.payload;
      })

      // --- Add reducer for logoutUser.fulfilled ---
      // This will reset the courses state when the user successfully logs out.
      .addCase(logoutUser.fulfilled, (state) => {
        // Reset to initial state or clear specific fields
        state.items = [];
        state.selectedCourse = null;
        state.loading = 'idle';
        state.selectedCourseLoading = 'idle';
        state.error = null;
        state.selectedCourseError = null;
        // Or, more simply, if you have a reset action:
        // return initialState; // This replaces the entire state with initialState
      });
  },
});

// Export the new resetCoursesState action if you added it
export const { clearCoursesError, clearSelectedCourse, clearSelectedCourseError, resetCoursesState } = coursesSlice.actions;
export default coursesSlice.reducer;