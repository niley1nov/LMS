// src/components/CourseDetail.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
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
import CircularProgress from '@mui/material/CircularProgress'; // For loading state
import Alert from '@mui/material/Alert'; // For error messages

// Icons for different unit types
import ArticleIcon from '@mui/icons-material/Article'; // For MATERIAL
import AssignmentIcon from '@mui/icons-material/Assignment'; // For ASSIGNMENT
import OndemandVideoIcon from '@mui/icons-material/OndemandVideo'; // For VIDEO
import QuizIcon from '@mui/icons-material/Quiz'; // For QUIZ
import ForumIcon from '@mui/icons-material/Forum'; // For DISCUSSION
import LinkIcon from '@mui/icons-material/Link'; // For EXTERNAL_LINK
import HelpOutlineIcon from '@mui/icons-material/HelpOutline'; // Default

export default function CourseDetail() {
  const { id } = useParams();
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true); // Start with loading true
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch(`${API_URL}/courses/${id}`, {
      credentials: "include",
    })
      .then(async (res) => { // Make async to await res.json() in error case
        if (!res.ok) {
          let errorMsg = `HTTP error ${res.status}`;
          try {
            const errorData = await res.json();
            errorMsg = errorData.detail || errorMsg;
          } catch (e) {
            // Ignore if response is not JSON
          }
          throw new Error(errorMsg);
        }
        return res.json();
      })
      .then((data) => {
        console.log(data);
        setCourse(data);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [API_URL, id]);

  const getUnitIcon = (unitType) => {
    switch (unitType?.toUpperCase()) { // Added optional chaining and toUpperCase for safety
      case 'MATERIAL':
        return <ArticleIcon />;
      case 'ASSIGNMENT':
        return <AssignmentIcon />;
      case 'VIDEO':
        return <OndemandVideoIcon />;
      case 'QUIZ':
        return <QuizIcon />;
      case 'DISCUSSION':
        return <ForumIcon />;
      case 'EXTERNAL_LINK':
        return <LinkIcon />;
      default:
        return <HelpOutlineIcon />;
    }
  };

  if (loading) {
    return (
      <Container sx={{ py: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography sx={{ mt: 2 }}>Loading course details…</Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ py: 4 }}>
        <Alert severity="error">Error loading course: {error}</Alert>
      </Container>
    );
  }

  if (!course) {
    // This case should ideally not be reached if loading and error are handled,
    // but as a fallback:
    return (
      <Container sx={{ py: 4 }}>
        <Typography>Course not found.</Typography>
      </Container>
    );
  }

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
              defaultExpanded={moduleIndex === 0} // Expand the first module by default
              sx={{ 
                mb: 2, 
                '&:before': { display: 'none' }, // Remove default top border
                boxShadow: '0px 3px 15px rgba(0,0,0,0.1)', // Softer shadow
                borderRadius: '8px',
              }}
            >
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls={`module-${module.id}-content`}
                id={`module-${module.id}-header`}
                sx={{ 
                  backgroundColor: 'primary.main', // Use theme primary color
                  color: 'primary.contrastText',
                  borderTopLeftRadius: '8px',
                  borderTopRightRadius: '8px',
                  borderBottomLeftRadius: module.units && module.units.length > 0 ? '0px' : '8px', // Keep rounded if no units
                  borderBottomRightRadius: module.units && module.units.length > 0 ? '0px' : '8px',
                  '& .MuiAccordionSummary-content': {
                    my: 1.5 // More padding inside summary
                  }
                }}
              >
                <Typography variant="h6" component="div" sx={{ fontWeight: 500 }}>
                  {`Module ${module.order || moduleIndex + 1}: ${module.title}`}
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
                        divider={unitIndex < module.units.length - 1} // Add divider except for the last item
                        sx={{ 
                            py: 1.5, 
                            px: 2,
                            '&:hover': { backgroundColor: 'action.hover' } 
                        }}
                        // component="a" href={unit.unit_type === 'EXTERNAL_LINK' ? unit.content : '#'} target="_blank" rel="noopener noreferrer" // Example: make link clickable
                      >
                        <ListItemIcon sx={{ minWidth: 40 }}>
                          {getUnitIcon(unit.type)} 
                          {/* The backend sends 'type', Pydantic schema aliases it to 'unit_type'.
                              If your frontend receives 'type', use unit.type.
                              If your frontend receives 'unit_type' (after Pydantic alias), use unit.unit_type.
                              Based on your schemas.py (UnitBase: unit_type: UnitType = Field(..., alias="type")),
                              the JSON response from FastAPI should have "type" as the key.
                          */}
                        </ListItemIcon>
                        <ListItemText 
                          primary={`${unit.order || unitIndex + 1}. ${unit.title}`} 
                          secondary={unit.content && unit.unit_type !== 'EXTERNAL_LINK' ? `Content: ${unit.content.substring(0,100)}${unit.content.length > 100 ? '...' : ''}` : (unit.unit_type === 'EXTERNAL_LINK' ? unit.content : null)}
                          primaryTypographyProps={{ fontWeight: 'medium' }}
                        />
                        {/* TODO: Add action buttons for unit (e.g., view, edit, delete based on role) */}
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
