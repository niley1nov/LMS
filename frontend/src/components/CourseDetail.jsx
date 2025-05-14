// src/components/CourseDetail.jsx
import React from "react";
import { useParams } from "react-router-dom";
import { useGetCourseByIdQuery } from "../redux/apiSlice";

import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import Box from "@mui/material/Box";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import CircularProgress from "@mui/material/CircularProgress";
import Alert from "@mui/material/Alert";

import ArticleIcon from "@mui/icons-material/Article";
import AssignmentIcon from "@mui/icons-material/Assignment";
import OndemandVideoIcon from "@mui/icons-material/OndemandVideo";
import QuizIcon from "@mui/icons-material/Quiz";
import ForumIcon from "@mui/icons-material/Forum";
import LinkIcon from "@mui/icons-material/Link";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";

const getUnitIcon = (type) => {
  switch (type?.toUpperCase()) {
    case "MATERIAL":
      return <ArticleIcon />;
    case "ASSIGNMENT":
      return <AssignmentIcon />;
    case "VIDEO":
      return <OndemandVideoIcon />;
    case "QUIZ":
      return <QuizIcon />;
    case "DISCUSSION":
      return <ForumIcon />;
    case "EXTERNAL_LINK":
      return <LinkIcon />;
    default:
      return <HelpOutlineIcon />;
  }
};

export default function CourseDetail() {
  const { id: courseId } = useParams();
  const {
    data: course,
    isLoading,
    isError,
    error,
  } = useGetCourseByIdQuery(courseId, { skip: !courseId });

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
      <Typography
        variant="h3"
        component="h1"
        gutterBottom
        sx={{ fontWeight: "bold" }}
      >
        {course.name}
      </Typography>
      <Divider sx={{ mb: 2 }} />
      <Typography
        variant="body1"
        paragraph
        sx={{ fontSize: "1.1rem", color: "text.secondary" }}
      >
        {course.description}
      </Typography>

      <Box sx={{ mt: 5 }}>
        <Typography variant="h5" component="h2" gutterBottom sx={{ mb: 3 }}>
          Course Content
        </Typography>
        {course.modules?.length > 0 ? (
          course.modules.map((module, idx) => (
            <Accordion
              key={module.id}
              defaultExpanded={idx === 0}
              sx={{
                mb: 2,
                "&:before": { display: "none" },
                boxShadow: "0px 3px 15px rgba(0,0,0,0.1)",
                borderRadius: "8px",
              }}
            >
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls={`module-${module.id}-content`}
                id={`module-${module.id}-header`}
                sx={{
                  backgroundColor: "primary.light",
                  color: "primary.contrastText",
                  borderTopLeftRadius: "8px",
                  borderTopRightRadius: "8px",
                  "& .MuiAccordionSummary-content": { my: 1.5 },
                }}
              >
                <Typography variant="h6" sx={{ fontWeight: 500 }}>
                  {`Module ${module.order ?? idx + 1}: ${module.title}`}
                </Typography>
              </AccordionSummary>

              <AccordionDetails
                sx={{
                  p: 0,
                  border: "1px solid",
                  borderColor: "divider",
                  borderTop: "none",
                  borderBottomLeftRadius: "8px",
                  borderBottomRightRadius: "8px",
                }}
              >
                {module.description && (
                  <Typography
                    variant="body2"
                    sx={{
                      p: 2,
                      color: "text.secondary",
                      borderBottom: "1px solid",
                      borderColor: "divider",
                    }}
                  >
                    {module.description}
                  </Typography>
                )}

                {module.units?.length > 0 ? (
                  <List dense disablePadding>
                    {module.units.map((unit, uidx) => (
                      <ListItem
                        key={unit.id}
                        divider={uidx < module.units.length - 1}
                        sx={{
                          py: 1.5,
                          px: 2,
                          "&:hover": { backgroundColor: "action.hover" },
                        }}
                      >
                        <ListItemIcon sx={{ minWidth: 40 }}>
                          {getUnitIcon(unit.type)}
                        </ListItemIcon>
                        <ListItemText
                          primary={`${unit.order ?? uidx + 1}. ${unit.title}`}
                          secondary={
                            unit.type === "EXTERNAL_LINK"
                              ? unit.content
                              : unit.content
                              ? `${unit.content.substring(0, 100)}${
                                  unit.content.length > 100 ? "..." : ""
                                }`
                              : null
                          }
                          primaryTypographyProps={{ fontWeight: "medium" }}
                        />
                      </ListItem>
                    ))}
                  </List>
                ) : (
                  <Typography
                    sx={{ p: 2, fontStyle: "italic", color: "text.disabled" }}
                  >
                    No units in this module yet.
                  </Typography>
                )}
              </AccordionDetails>
            </Accordion>
          ))
        ) : (
          <Typography
            sx={{ fontStyle: "italic", color: "text.disabled", mt: 2 }}
          >
            No modules have been added to this course yet.
          </Typography>
        )}
      </Box>
    </Container>
  );
}
