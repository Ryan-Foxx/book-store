import { useDispatch, useSelector } from "react-redux";
import type { AppDispatch, RootState } from "./store";

// Type-Safe Version For Use In Components
export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();
