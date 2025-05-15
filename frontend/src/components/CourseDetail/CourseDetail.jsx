// src/components/CourseDetail.jsx
import React, { useState, useEffect } from "react";
import { Tabs, Tab } from "@mui/material";
import { useParams, useLocation, Outlet } from "react-router-dom";
import { useGetCourseByIdQuery } from "../../redux/apiSlice";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";
import TabPanel from "./tabs/TabPanel";
import StreamTab from "./tabs/StreamTab";
import ClassworkTab from "./tabs/ClassworkTab";
import PeopleTab from "./tabs/PeopleTab";
import MarksTab from "./tabs/MarksTab";

export default function CourseDetail() {
  const { courseId } = useParams();
  const {
    data: course,
    isLoading,
    isError,
    error,
  } = useGetCourseByIdQuery(courseId, { skip: !courseId });

  const location = useLocation();
  // initialize from navigation state if present
  const [tabIndex, setTabIndex] = useState(
    () => location.state?.initialTab ?? 0
  );

  useEffect(() => {
    if (typeof location.state?.initialTab === "number") {
      setTabIndex(location.state.initialTab);
    }
  }, [location.state]);

  if (isLoading) {
    return (
      <Container sx={{ py: 4, textAlign: "center" }}>
        <CircularProgress />
        <Typography sx={{ mt: 2 }}>Loading course details…</Typography>
      </Container>
    );
  }

  if (isError) {
    const message =
      error?.data?.detail || error?.error || "Failed to load course.";
    return (
      <Container sx={{ py: 4 }}>
        <Alert severity="error">Error: {message}</Alert>
      </Container>
    );
  }

  if (!course) {
    return (
      <Container sx={{ py: 4 }}>
        <Alert severity="warning">Course not found.</Alert>
      </Container>
    );
  }

  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h3" gutterBottom sx={{ fontWeight: "bold" }}>
        {course.name}
      </Typography>
      <Divider sx={{ mb: 2 }} />

      <Tabs
        value={tabIndex}
        onChange={(_, v) => setTabIndex(v)}
        textColor="primary"
        indicatorColor="primary"
        sx={{ mb: 4 }}
      >
        <Tab label="Stream" />
        <Tab label="Classwork" />
        <Tab label="People" />
        <Tab label="Marks" />
      </Tabs>

      <TabPanel value={tabIndex} index={0}>
        <StreamTab />
      </TabPanel>
      <TabPanel value={tabIndex} index={1}>
        <ClassworkTab modules={course.modules} />
      </TabPanel>
      <TabPanel value={tabIndex} index={2}>
        <PeopleTab />
      </TabPanel>
      <TabPanel value={tabIndex} index={3}>
        <MarksTab />
      </TabPanel>
    </Container>
  );
}
