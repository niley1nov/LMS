// src/redux/authSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import apiService from './apiService'; // Use the centralized API service

// Async thunk for fetching the current user
export const fetchCurrentUser = createAsyncThunk(
  'auth/fetchCurrentUser',
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiService.get('/users/me');
      return response.data;
    } catch (error) {
      if (error.response && error.response.status === 401) {
        return rejectWithValue('Not authenticated'); // Specific message for 401
      }
      return rejectWithValue(error.response?.data?.detail || error.message || 'Failed to fetch user');
    }
  }
);

// Async thunk for Google login
export const loginWithGoogle = createAsyncThunk(
  'auth/loginWithGoogle',
  async (googleIdToken, { dispatch, rejectWithValue }) => {
    try {
      const response = await apiService.post('/auth/google', { token: googleIdToken });
      // After successful backend login, fetch the user details again to ensure fresh state
      // or trust the user object returned by the login endpoint.
      // Here, we assume the /auth/google endpoint returns the user object.
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || error.message || 'Google login failed');
    }
  }
);

// Async thunk for logout
export const logoutUser = createAsyncThunk(
  'auth/logoutUser',
  async (_, { rejectWithValue }) => {
    try {
      await apiService.post('/auth/logout', {});
      return null; // Indicate successful logout
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || error.message || 'Logout failed');
    }
  }
);

const initialState = {
  user: null,
  isAuthenticated: false, // More explicit than just checking user
  loading: 'idle', // 'idle' | 'pending' | 'succeeded' | 'failed'
  initialAuthCheckDone: false, // To track if initial fetchCurrentUser has completed
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    // You could add a reducer to manually set user if needed, e.g., from SSR
    // setUser: (state, action) => {
    //   state.user = action.payload;
    //   state.isAuthenticated = !!action.payload;
    // },
    clearAuthError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // fetchCurrentUser
      .addCase(fetchCurrentUser.pending, (state) => {
        state.loading = 'pending';
        state.error = null;
      })
      .addCase(fetchCurrentUser.fulfilled, (state, action) => {
        state.loading = 'succeeded';
        state.user = action.payload;
        state.isAuthenticated = true;
        state.initialAuthCheckDone = true;
      })
      .addCase(fetchCurrentUser.rejected, (state, action) => {
        state.loading = 'failed';
        state.user = null;
        state.isAuthenticated = false;
        state.error = action.payload; // Error message from rejectWithValue
        state.initialAuthCheckDone = true;
      })
      // loginWithGoogle
      .addCase(loginWithGoogle.pending, (state) => {
        state.loading = 'pending';
        state.error = null;
      })
      .addCase(loginWithGoogle.fulfilled, (state, action) => {
        state.loading = 'succeeded';
        state.user = action.payload;
        state.isAuthenticated = true;
      })
      .addCase(loginWithGoogle.rejected, (state, action) => {
        state.loading = 'failed';
        state.user = null;
        state.isAuthenticated = false;
        state.error = action.payload;
      })
      // logoutUser
      .addCase(logoutUser.pending, (state) => {
        state.loading = 'pending';
      })
      .addCase(logoutUser.fulfilled, (state) => {
        state.loading = 'succeeded';
        state.user = null;
        state.isAuthenticated = false;
        state.error = null;
      })
      .addCase(logoutUser.rejected, (state, action) => {
        state.loading = 'failed';
        // Even if backend logout fails, we clear user locally for UX
        state.user = null;
        state.isAuthenticated = false;
        state.error = action.payload;
      });
  },
});

export const { clearAuthError } = authSlice.actions;
export default authSlice.reducer;