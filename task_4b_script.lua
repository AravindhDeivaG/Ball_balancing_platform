--[[
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This Lua script is to implement Task 4B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
]]--


--[[
# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_4b_lua
# Functions:        [ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]
]]--

--[[
##################### GLOBAL VARIABLES #######################
## You can add global variables in this section according   ##
## to your requirement.                                     ##
## DO NOT TAMPER WITH THE ALREADY DEFINED GLOBAL VARIABLES. ##
##############################################################
]]--

maze_array = {}
baseHandle = -1       --Do not change or delete this variable
textureID = -1        --Do not change or delete this variable
textureData = -1       --Do not change or delete this variable
base_children_list={} --Do not change or delete this variable
baseHandle = -1       --Do not change or delete this variable

--############################################################

--[[
##################### HELPER FUNCTIONS #######################
## You can add helper functions in this section according   ##
## to your requirement.                                     ##
## DO NOT MODIFY OR CHANGE THE ALREADY DEFINED HELPER       ##
## FUNCTIONS                                                ##
##############################################################
]]--

--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION
**************************************************************
	Function Name : createWall()
	Purpose:
	---
	Creates a black-colored wall of dimensions 90cm x 10cm x 10cm

	Input Arguments:
	---
	None
	
	Returns:
	---
	wallObjectHandle : number
	
	returns the object handle of the wall created
	
	Example call:
	---
	wallObjectHandle = createWall()
**************************************************************	
]]--
function createWall()
	wallObjectHandle = sim.createPureShape(0, 8, {0.09, 0.01, 0.1}, 0.0001, nil)
	--Refer https://www.coppeliarobotics.com/helpFiles/en/regularApi/simCreatePureShape.htm to understand the parameters passed to this function
	sim.setShapeColor(wallObjectHandle, nil, sim.colorcomponent_ambient_diffuse, {0, 0, 0})
	sim.setObjectInt32Parameter(wallObjectHandle,sim.shapeintparam_respondable_mask,65280)
	--Refer https://www.coppeliarobotics.com/helpFiles/en/apiFunctions.htm#sim.setObjectInt32Parameter to understand the various parameters passed. 	
	--The walls should only be collidable with the ball and not with each other.
	--Hence we are enabling only the local respondable masks of the walls created.
	sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_collidable)
	--Walls may have to be set as renderable........................... 
	--This is required to make the wall as collidable
	return wallObjectHandle
end

--############################################################

--[[
**************************************************************
	Function Name : receiveData()
	Purpose:
	---
	Receives data via Remote API. This function is called by 
	simx.callScriptFunction() in the python code (task_2b.py)

	Input Arguments:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	These 4 variables represent the data being passed from remote
	API client(python) to the CoppeliaSim scene
	
	Example call:
	---
	Shall be called from the python script
**************************************************************	
]]--
function receiveData(inInts,inFloats,inStrings,inBuffer)

	--*******************************************************
	--               ADD YOUR CODE HERE
	
	maze_array = inInts


	--*******************************************************
	return inInts, inFloats, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : generateHorizontalWalls()
	Purpose:
	---
	Generates all the Horizontal Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	generateHorizontalWalls()
**************************************************************	
]]--
function generateHorizontalWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
	
         position = {}
         b = {}
         
         position[2] = 6.0000e-01 + 0.0000e+00
         for j = 1,11,1 do
         b[j] = {}
         position[1] = -5.5000e-01 + 5.7062e-07
         position[2] = position[2] - 1.0000e-01
         for i =1,10,1 do
         position[1] = position[1] + 1.0000e-01
         position[3] = 0.09
         baseHandle = sim.getObjectHandle("force_sensor_pw_1")
         a = createWall()
         b[j][i] = a
         sim.setObjectParent(a,baseHandle,keepInPlace)
         sim.setObjectPosition(a,sim.handle_parent,position)
         end
         end 

	--*******************************************************
end

--[[
**************************************************************
	Function Name : generateVerticalWalls()
	Purpose:
	---
	Generates all the Vertical Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	generateVerticalWalls()
**************************************************************	
]]--
function generateVerticalWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
	
         position = {}
         c = {}
         eulerAngles = {0,0,math.pi/2}
         position[2] = 5.5000e-01 + 0.0000e+00
         for j = 1,10,1 do
         c[j] = {}
         position[1] = -6.0000e-01 + 5.7062e-07
         position[2] = position[2] - 1.0000e-01
         for i =1,11,1 do
         position[1] = position[1] + 1.0000e-01
         position[3] = 0.09
         baseHandle = sim.getObjectHandle("force_sensor_pw_1")
         a = createWall()
         c[j][i] = a
         sim.setObjectOrientation(a,sim.handle_parent,eulerAngles)
         sim.setObjectParent(a,baseHandle,keepInPlace)
         sim.setObjectPosition(a,sim.handle_parent,position)
         end
         end

	--*******************************************************
end

--[[
**************************************************************
	Function Name : deleteWalls()
	Purpose:
	---
	Deletes all the grouped walls in the given scene

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	deleteWalls()
**************************************************************	
]]--
function deleteWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
        
		walls_1 = sim.getObjectHandle("walls_1")
        sim.removeObject(walls_1)
		
	--*******************************************************
end


--[[
**************************************************************
  YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT PARAMETERS FOR THIS
						  FUNCTION
**************************************************************
	Function Name : createMaze()
	Purpose:
	---
	Creates the maze in the given scene by deleting specific 
	horizontal and vertical walls

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	createMaze()
**************************************************************	
]]--
function createMaze()
	
	--*******************************************************
	--               ADD YOUR CODE HERE
	
    k = 1
    ar = {}
    for i = 1, 10, 1 do
    ar[i] = {}
    for j = 1, 10, 1 do
    ar[i][j] = maze_array[k]
    k = k+1
    end
    end
              
    for j = 1, 10, 1 do
    for k = 1, 10, 1 do
     if ( k ~= 10 and j ~= 10 ) then
      if ar[j][k] == 0 
         then sim.removeObject(b[j][k])
              sim.removeObject(c[j][k]) 
           
           elseif ar[j][k] == 1 
         then sim.removeObject(b[j][k])
              
           elseif ar[j][k] == 2 
         then sim.removeObject(c[j][k]) 
            
           elseif ar[j][k] == 4 
         then sim.removeObject(b[j][k]) 
              sim.removeObject(c[j][k]) 
             
           elseif ar[j][k] == 5 
         then sim.removeObject(b[j][k]) 
          
           elseif ar[j][k] == 6 
         then sim.removeObject(c[j][k]) 
       
           elseif ar[j][k] == 8 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(b[j][k]) 
              
           elseif ar[j][k] == 9 
         then sim.removeObject(b[j][k]) 
              
           elseif ar[j][k] == 10 
         then sim.removeObject(c[j][k]) 
              
           elseif ar[j][k] == 12 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(b[j][k]) 
           elseif ar[j][k] == 13 
         then sim.removeObject(b[j][k]) 
           elseif ar[j][k] == 14
         then sim.removeObject(c[j][k]) 
           else
      end
      end
         if ( k == 10 and j ~= 10 ) then
               if ar[j][k] == 0 
         then sim.removeObject(b[j][k])
              sim.removeObject(c[j][k]) 
              sim.removeObject(c[j][k+1]) 
              
           elseif ar[j][k] == 1 
         then sim.removeObject(b[j][k])
              sim.removeObject(c[j][k+1])
               
           elseif ar[j][k] == 2 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(c[j][k+1]) 
                
           elseif ar[j][k] == 3 
         then sim.removeObject(c[j][k+1]) 
             
           elseif ar[j][k] == 4 
         then sim.removeObject(b[j][k]) 
              sim.removeObject(c[j][k]) 
           
           elseif ar[j][k] == 5 
         then sim.removeObject(b[j][k]) 
              
           elseif ar[j][k] == 6 
         then sim.removeObject(c[j][k]) 
              
         
           elseif ar[j][k] == 8 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(b[j][k]) 
              sim.removeObject(c[j][k+1]) 
           elseif ar[j][k] == 9 
         then sim.removeObject(b[j][k]) 
              sim.removeObject(c[j][k+1]) 
           elseif ar[j][k] == 10 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(c[j][k+1]) 
           elseif ar[j][k] == 11 
         then sim.removeObject(c[j][k+1]) 
           elseif ar[j][k] == 12 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(b[j][k]) 
           elseif ar[j][k] == 13 
         then sim.removeObject(b[j][k]) 
           elseif ar[j][k] == 14
         then sim.removeObject(c[j][k]) 
           else
      end
      end
         if ( k ~= 10 and j == 10 ) then
              if ar[j][k] == 0 
         then sim.removeObject(b[j][k])
              sim.removeObject(c[j][k]) 
              sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 1 
         then sim.removeObject(b[j][k])
              sim.removeObject(b[j+1][k])  
           elseif ar[j][k] == 2 
         then sim.removeObject(c[j][k]) 
               
              sim.removeObject(b[j+1][k])   
           elseif ar[j][k] == 3 
         then 
              sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 4 
         then sim.removeObject(b[j][k]) 
              sim.removeObject(c[j][k]) 
              sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 5 
         then sim.removeObject(b[j][k]) 
              sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 6 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 7 
         then sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 8 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(b[j][k]) 
            
           elseif ar[j][k] == 9 
         then sim.removeObject(b[j][k]) 
              
           elseif ar[j][k] == 10 
         then sim.removeObject(c[j][k]) 
            
           
           elseif ar[j][k] == 12 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(b[j][k]) 
           elseif ar[j][k] == 13 
         then sim.removeObject(b[j][k]) 
           elseif ar[j][k] == 14
         then sim.removeObject(c[j][k]) 
           else
      end
      end
         if ( k == 10 and j == 10 ) then
               if ar[j][k] == 0 
         then sim.removeObject(b[j][k])
              sim.removeObject(c[j][k]) 
              sim.removeObject(c[j][k+1]) 
              sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 1 
         then sim.removeObject(b[j][k])
              sim.removeObject(c[j][k+1])
              sim.removeObject(b[j+1][k])  
           elseif ar[j][k] == 2 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(c[j][k+1]) 
              sim.removeObject(b[j+1][k])   
           elseif ar[j][k] == 3 
         then sim.removeObject(c[j][k+1]) 
              sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 4 
         then sim.removeObject(b[j][k]) 
              sim.removeObject(c[j][k]) 
              sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 5 
         then sim.removeObject(b[j][k]) 
              sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 6 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 7 
         then sim.removeObject(b[j+1][k]) 
           elseif ar[j][k] == 8 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(b[j][k]) 
              sim.removeObject(c[j][k+1]) 
           elseif ar[j][k] == 9 
         then sim.removeObject(b[j][k]) 
              sim.removeObject(c[j][k+1]) 
           elseif ar[j][k] == 10 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(c[j][k+1]) 
           elseif ar[j][k] == 11 
         then sim.removeObject(c[j][k+1]) 
           elseif ar[j][k] == 12 
         then sim.removeObject(c[j][k]) 
              sim.removeObject(b[j][k]) 
           elseif ar[j][k] == 13 
         then sim.removeObject(b[j][k]) 
           elseif ar[j][k] == 14
         then sim.removeObject(c[j][k]) 
           else
      end
      end
         
 end
end

	--*******************************************************
end
--[[
	Function Name : groupWalls()
	Purpose:
	---
	Groups the various walls in the scene to one object.
	The name of the new grouped object should be set as 'walls_1'.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	groupWalls()
**************************************************************	
]]--

function groupWalls()
	--*******************************************************
	--               ADD YOUR CODE HERE
    kiara = {}
    bh = 1
  
    for j = 1,10,1 do
    for i =1,11,1 do
    result=sim.isHandleValid(c[j][i],-1)
    
    if result == 1 then
    kiara[bh] = c[j][i]
    bh = bh + 1
    end 
    
    end
    end
	
    for j = 1,11,1 do
    for i =1,10,1 do
    result=sim.isHandleValid(b[j][i],-1)

    if result == 1 then
    kiara[bh] = b[j][i]
    bh = bh + 1 
    end
    
    end
    end
	
    walls_1=sim.groupShapes(kiara,false)
    sim.setObjectName(walls_1,"walls_1")
	

	--*******************************************************
end

--[[
	Function Name : addToCollection()
	Purpose:
	---
	Adds the 'walls_1' grouped object to the collection 'colliding_objects'.  

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	addToCollection()
**************************************************************	
]]--

function addToCollection()
	--*******************************************************
	--               ADD YOUR CODE HERE
        colliding_objects=sim.getCollectionHandle("colliding_objects")
        walls_1 = sim.getObjectHandle("walls_1")
        sim.addObjectToCollection(colliding_objects,walls_1,sim.handle_single,0)


	--*******************************************************
end

--[[
	******************************************************************************
			YOU ARE ALLOWED TO MODIFY THIS FUNCTION DEPENDING ON YOUR PATH. 
	******************************************************************************
	Function Name : drawPath(inInts,path,inStrings,inBuffer)
	Purpose:
	---
	Builds blue coloured lines in the scene according to the
	path generated from the python file. 

	Input Arguments:
	---
	inInts : Table of Ints
	inFloats : Table of Floats (containing the path generated)
	inStrings : Table of Strings
	inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	Example call:
	---
	Shall be called from the python script
**************************************************************	
]]--

function drawPath(inInts,path,inStrings,inBuffer)
	--[[posTable=sim.getObjectPosition(wallsGroupHandle,-1)
	print('=========================================')
	print('Path received is as follows: ')
	print(path)
	if not lineContainer then
		_lineContainer=sim.addDrawingObject(sim.drawing_lines,1,0,wallsGroupHandle,99999,{0.2,0.2,1})
		sim.addDrawingObjectItem(_lineContainer,nil)
		if path then
			local pc=#path/2
			for i=1,pc-1,1 do
				lineDat={path[(i-1)*2+1],path[(i-1)*2+2],posTable[3]-0.03,path[(i)*2+1],path[(i)*2+2],posTable[3]-0.03}
				sim.addDrawingObjectItem(_lineContainer,lineDat)
			end
		end
	end
	return inInts, path, inStrings, inBuffer
    ]]--
    return {},{},{},""
end

--[[
**************************************************************
	Function Name : sysCall_init()
	Purpose:
	---
	Can be used for initialization of parameters
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_init()
	--*******************************************************
	--               ADD YOUR CODE HERE
 
	--*******************************************************
end

--[[
**************************************************************
		YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION.
		YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT 
		PARAMETERS ONLY FOR CREATEMAZE() FUNCTION
**************************************************************
	Function Name : sysCall_beforeSimulation()
	Purpose:
	---
	This is executed before simulation starts
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_beforeSimulation()
	
	generateHorizontalWalls()
	generateVerticalWalls()
	createMaze()--You can define your own input and output parameters only for this function
	groupWalls()
	addToCollection()
end

--[[
**************************************************************
		YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION. 
**************************************************************
	Function Name : sysCall_afterSimulation()
	Purpose:
	---
	This is executed after simulation ends
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_afterSimulation()
	-- is executed after a simulation ends
	deleteWalls()
    evaluation_screen_respondable=sim.getObjectHandle('evaluation_screen_respondable@silentError')
    if(evaluation_screen_respondable~=-1) then
        sim.removeModel(evaluation_screen_respondable)
    end
end

function sysCall_cleanup()
	-- do some clean-up here
end

-- See the user manual or the available code snippets for additional callback functions and details
