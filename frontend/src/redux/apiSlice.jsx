// src/redux/apiSlice.js
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.REACT_APP_API_BASE_URL,
    credentials: "include",
  }),
  tagTypes: ["User", "Courses", "Modules", "Units"],
  endpoints: (builder) => ({
    // Fetch current user
    getCurrentUser: builder.query({
      query: () => "/users/me",
      providesTags: ["User"],
    }),

    // Google login
    loginWithGoogle: builder.mutation({
      query: (googleIdToken) => ({
        url: "/auth/google",
        method: "POST",
        body: { token: googleIdToken },
      }),
      invalidatesTags: ["User"],
    }),

    // Logout
    logoutUser: builder.mutation({
      query: () => ({
        url: "/auth/logout",
        method: "POST",
      }),
      invalidatesTags: ["User", "Courses"],
    }),

    // Courses list
    getCourses: builder.query({
      query: () => "/courses",
      providesTags: ["Courses"],
      keepUnusedDataFor: 0,
    }),

    // Course detail
    getCourseById: builder.query({
      query: (id) => `/courses/${id}`,
      providesTags: (result, error, id) => [{ type: "Courses", id }],
      keepUnusedDataFor: 0,
    }),

    // Create new course
    createCourse: builder.mutation({
      query: (courseData) => ({
        url: "/courses",
        method: "POST",
        body: courseData,
      }),
      invalidatesTags: ["Courses"],
    }),

    getModulesByCourse: builder.query({
      query: (courseId) => `/courses/${courseId}/modules`,
      providesTags: (result, error, courseId) =>
        result
          ? [
              ...result.map((m) => ({ type: "Modules", id: m.id })),
              { type: "Modules", id: `COURSE_${courseId}` },
            ]
          : [{ type: "Modules", id: `COURSE_${courseId}` }],
      keepUnusedDataFor: 0,
    }),
    createModule: builder.mutation({
      query: ({ courseId, ...moduleData }) => ({
        url: `/courses/${courseId}/modules`,
        method: "POST",
        body: moduleData,
      }),
      invalidatesTags: (result, error, { courseId }) => [
        { type: "Modules", id: `COURSE_${courseId}` },
        { type: "Courses", id: courseId },
      ],
    }),

    // ── Units ──
    getUnitsByModule: builder.query({
      query: (moduleId) => `/modules/${moduleId}/units`,
      providesTags: (result, error, moduleId) =>
        result
          ? [
              ...result.map((u) => ({ type: "Units", id: u.id })),
              { type: "Units", id: `MODULE_${moduleId}` },
            ]
          : [{ type: "Units", id: `MODULE_${moduleId}` }],
      keepUnusedDataFor: 0,
    }),
    createUnit: builder.mutation({
      query: ({ moduleId, ...unitData }) => ({
        url: `/modules/${moduleId}/units`,
        method: "POST",
        body: unitData,
      }),
      // instead of invalidating, we optimistically merge the new unit
      async onQueryStarted({ moduleId, courseId }, { dispatch, queryFulfilled }) {
        try {
          const { data: newUnit } = await queryFulfilled;
          // insert into the cached CourseDetail
          dispatch(
            api.util.updateQueryData(
              "getCourseById",
              courseId,
              (draft) => {
                const mod = draft.modules.find((m) => String(m.id) === moduleId);
                if (mod) {
                  mod.units.push(newUnit);
                }
              }
            )
          );
        } catch {
          // nothing—error will be surfaced to the component
        }
      },
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
  useGetModulesByCourseQuery,
  useCreateModuleMutation,
  useGetUnitsByModuleQuery,
  useCreateUnitMutation,
} = api;
