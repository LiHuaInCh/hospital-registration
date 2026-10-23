package com.hospital.controller;

import com.hospital.common.R;
import com.hospital.entity.Department;
import com.hospital.service.DepartmentService;
import com.hospital.vo.DepartmentVO;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/department")
@RequiredArgsConstructor
public class DepartmentController {

    private final DepartmentService departmentService;

    @GetMapping("/list")
    public R<List<DepartmentVO>> list() {
        return R.ok(departmentService.listActive());
    }

    @GetMapping("/detail")
    public R<Department> detail(@RequestParam Long id) {
        return R.ok(departmentService.detail(id));
    }

    @PostMapping("/add")
    public R<Department> add(@RequestBody Department department) {
        return R.ok(departmentService.create(department));
    }

    @PutMapping("/update")
    public R<Department> update(@RequestBody Department department) {
        if (department.getId() == null) {
            return R.fail("缺少科室标识");
        }
        return R.ok(departmentService.update(department.getId(), department));
    }

    @DeleteMapping("/delete")
    public R<Void> delete(@RequestParam Long id) {
        departmentService.delete(id);
        return R.ok();
    }
}
