// src/components/CourseDetail.jsx
import React, { useEffect } from "react"; // Removed useState
import { useParams } from "react-router-dom";
// 1. Import Redux hooks and actions
import { useDispatch, useSelector } from "react-redux";
import { fetchCourseById, clearSelectedCourse, clearSelectedCourseError } from "../redux/coursesSlice"; // Ensure correct path

import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import Box from "@mui/material/Box";
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';

// Icons
import ArticleIcon from '@mui/icons-material/Article';
import AssignmentIcon from '@mui/icons-material/Assignment';
import OndemandVideoIcon from '@mui/icons-material/OndemandVideo';
import QuizIcon from '@mui/icons-material/Quiz';
import ForumIcon from '@mui/icons-material/Forum';
import LinkIcon from '@mui/icons-material/Link';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

export default function CourseDetail() {
  const { id: courseId } = useParams(); // Get courseId from URL params
  const dispatch = useDispatch();

  // 2. Get state from Redux store using specific selectors for clarity
  const { 
    selectedCourse, 
    selectedCourseLoading: loading, // Use specific loading state from slice
    selectedCourseError: error     // Use specific error state from slice
  } = useSelector((state) => state.courses);
  
  // Optional: get auth state if needed for conditional rendering within this component
  // const { isAuthenticated, user, loading: authLoading } = useSelector((state) => state.auth);

  useEffect(() => {
    if (courseId) {
      dispatch(clearSelectedCourseError()); // Clear previous errors for this specific view
      dispatch(fetchCourseById(courseId));
    }
    // Cleanup function to clear selected course when component unmounts or courseId changes
    return () => {
      dispatch(clearSelectedCourse());
    };
  }, [dispatch, courseId]); // Re-fetch if courseId changes

  const getUnitIcon = (unitType) => {
    // The backend JSON response should have "type" due to Pydantic alias.
    // So, unit.type is correct here.
    switch (unitType?.toUpperCase()) { 
      case 'MATERIAL': return <ArticleIcon />;
      case 'ASSIGNMENT': return <AssignmentIcon />;
      case 'VIDEO': return <OndemandVideoIcon />;
      case 'QUIZ': return <QuizIcon />;
      case 'DISCUSSION': return <ForumIcon />;
      case 'EXTERNAL_LINK': return <LinkIcon />;
      default: return <HelpOutlineIcon />;
    }
  };

  // Use the specific loading state from the courses slice
  if (loading === 'pending') {
    return (
      <Container sx={{ py: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography sx={{ mt: 2 }}>Loading course details…</Typography>
      </Container>
    );
  }

  // Use the specific error state
  if (error && loading === 'failed') {
    return (
      <Container sx={{ py: 4 }}>
        <Alert severity="error">Error loading course: {typeof error === 'string' ? error : "An unknown error occurred."}</Alert>
      </Container>
    );
  }

  // If loading succeeded but no course was found (e.g., 404 from backend, handled by thunk)
  if (!selectedCourse && loading === 'succeeded') {
    return (
      <Container sx={{ py: 4 }}>
        <Alert severity="warning">Course not found.</Alert>
      </Container>
    );
  }
  
  // Fallback if still no course (e.g., initial render before loading has properly started and set to 'pending')
  // This check might be redundant if the loading === 'pending' check above is sufficient
  if (!selectedCourse) { 
      return (
          <Container sx={{ py: 4, textAlign: 'center' }}>
            {/* Can show a more subtle loader or placeholder here if preferred over just text */}
            {/* <Typography>Preparing course data...</Typography> */}
            <CircularProgress size={24} /> 
          </Container>
      );
  }

  // At this point, selectedCourse should be available
  const course = selectedCourse;

  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        {course.name}
      </Typography>
      <Divider sx={{ mb: 2 }} />
      <Typography variant="body1" paragraph sx={{ fontSize: '1.1rem', color: 'text.secondary' }}>
        {course.description}
      </Typography>

      <Box sx={{ mt: 5 }}>
        <Typography variant="h5" component="h2" gutterBottom sx={{ mb: 3 }}>
          Course Content
        </Typography>
        {course.modules && course.modules.length > 0 ? (
          course.modules.map((module, moduleIndex) => (
            <Accordion 
              key={module.id} 
              defaultExpanded={moduleIndex === 0}
              sx={{ 
                mb: 2, 
                '&:before': { display: 'none' },
                boxShadow: '0px 3px 15px rgba(0,0,0,0.1)',
                borderRadius: '8px',
              }}
            >
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls={`module-${module.id}-content`}
                id={`module-${module.id}-header`}
                sx={{ 
                  backgroundColor: 'primary.light',
                  color: 'primary.contrastText',
                  borderTopLeftRadius: '8px',
                  borderTopRightRadius: '8px',
                  borderBottomLeftRadius: module.units && module.units.length > 0 ? '0px' : '8px',
                  borderBottomRightRadius: module.units && module.units.length > 0 ? '0px' : '8px',
                  '& .MuiAccordionSummary-content': { my: 1.5 }
                }}
              >
                <Typography variant="h6" component="div" sx={{ fontWeight: 500 }}>
                  {`Module ${module.order !== undefined ? module.order : moduleIndex + 1}: ${module.title}`}
                </Typography>
              </AccordionSummary>
              <AccordionDetails sx={{ p: 0, border: '1px solid', borderColor: 'divider', borderTop: 'none', borderBottomLeftRadius: '8px', borderBottomRightRadius: '8px' }}>
                {module.description && (
                    <Typography variant="body2" sx={{ p: 2, color: 'text.secondary', borderBottom: '1px solid', borderColor: 'divider' }}>
                        {module.description}
                    </Typography>
                )}
                {module.units && module.units.length > 0 ? (
                  <List dense disablePadding>
                    {module.units.map((unit, unitIndex) => (
                      <ListItem 
                        key={unit.id} 
                        divider={unitIndex < module.units.length - 1}
                        sx={{ py: 1.5, px: 2, '&:hover': { backgroundColor: 'action.hover' } }}
                      >
                        <ListItemIcon sx={{ minWidth: 40 }}>
                          {getUnitIcon(unit.type)} {/* Assuming API returns 'type' */}
                        </ListItemIcon>
                        <ListItemText 
                          primary={`${unit.order !== undefined ? unit.order : unitIndex + 1}. ${unit.title}`} 
                          secondary={unit.content && unit.type !== 'EXTERNAL_LINK' 
                            ? `Content: ${unit.content.substring(0,100)}${unit.content.length > 100 ? '...' : ''}` 
                            : (unit.type === 'EXTERNAL_LINK' ? unit.content : null)}
                          primaryTypographyProps={{ fontWeight: 'medium' }}
                        />
                      </ListItem>
                    ))}
                  </List>
                ) : (
                  <Typography sx={{ p: 2, fontStyle: 'italic', color: 'text.disabled' }}>
                    No units in this module yet.
                  </Typography>
                )}
              </AccordionDetails>
            </Accordion>
          ))
        ) : (
          <Typography sx={{ fontStyle: 'italic', color: 'text.disabled', mt: 2 }}>
            No modules have been added to this course yet.
          </Typography>
        )}
      </Box>
    </Container>
  );
}