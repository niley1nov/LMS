// src/redux/apiSlice.js
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.REACT_APP_API_BASE_URL,
    credentials: 'include',
  }),
  tagTypes: ['User', 'Courses'],
  endpoints: builder => ({
    // Fetch current user
    getCurrentUser: builder.query({
      query: () => '/users/me',
      providesTags: ['User'],
    }),

    // Google login
    loginWithGoogle: builder.mutation({
      query: googleIdToken => ({
        url: '/auth/google',
        method: 'POST',
        body: { token: googleIdToken },
      }),
      invalidatesTags: ['User'],
    }),

    // Logout
    logoutUser: builder.mutation({
      query: () => ({
        url: '/auth/logout',
        method: 'POST',
      }),
      invalidatesTags: ['User', 'Courses'],
    }),

    // Courses list
    getCourses: builder.query({
      query: () => '/courses',
      providesTags: ['Courses'],
      keepUnusedDataFor: 0,
    }),

    // Course detail
    getCourseById: builder.query({
      query: id => `/courses/${id}`,
      providesTags: (result, error, id) => [{ type: 'Courses', id }],
      keepUnusedDataFor: 0,
    }),

    // Create new course
    createCourse: builder.mutation({
      query: courseData => ({
        url: '/courses',
        method: 'POST',
        body: courseData,
      }),
      invalidatesTags: ['Courses'],
    }),
  }),
});

export const {
  useGetCurrentUserQuery,
  useLoginWithGoogleMutation,
  useLogoutUserMutation,
  useGetCoursesQuery,
  useGetCourseByIdQuery,
  useCreateCourseMutation,
} = api;