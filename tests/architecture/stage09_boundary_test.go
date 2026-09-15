package architecture

import (
	"go/ast"
	"go/parser"
	"go/token"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestStage09EinoImportsStayBehindAdapterBoundary(t *testing.T) {
	root := repoRoot(t)
	var offenders []string

	walkGoFiles(t, root, func(path string) {
		rel := slashRel(t, root, path)
		if !strings.HasPrefix(rel, "internal/") && !strings.HasPrefix(rel, "apps/") && !strings.HasPrefix(rel, "tests/") {
			return
		}
		if strings.HasSuffix(rel, "_test.go") {
			return
		}

		file := parseFile(t, path)
		for _, imp := range file.Imports {
			importPath := strings.Trim(imp.Path.Value, `"`)
			if strings.HasPrefix(importPath, "github.com/cloudwego/eino") &&
				!strings.HasPrefix(rel, "internal/platform/runtime/eino/") {
				offenders = append(offenders, rel+" imports "+importPath)
			}
		}
	})

	if len(offenders) > 0 {
		t.Fatalf("Eino leaked outside runtime adapter boundary:\n%s", strings.Join(offenders, "\n"))
	}
}

func TestStage09NoPrematureDistributedInfrastructureImports(t *testing.T) {
	root := repoRoot(t)
	forbidden := []string{"redis", "dbos", "pgx", "postgres", "kafka", "celery"}
	var offenders []string

	walkGoFiles(t, root, func(path string) {
		rel := slashRel(t, root, path)
		if strings.HasPrefix(rel, "stage-09-single-process-runtime-v0.1/") {
			return
		}

		file := parseFile(t, path)
		for _, imp := range file.Imports {
			importPath := strings.ToLower(strings.Trim(imp.Path.Value, `"`))
			for _, denied := range forbidden {
				if strings.Contains(importPath, denied) {
					offenders = append(offenders, rel+" imports "+importPath)
				}
			}
		}
	})

	if len(offenders) > 0 {
		t.Fatalf("Stage 09 imported deferred infrastructure:\n%s", strings.Join(offenders, "\n"))
	}
}

func repoRoot(t *testing.T) string {
	t.Helper()
	wd, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	for {
		if _, err := os.Stat(filepath.Join(wd, "go.mod")); err == nil {
			return wd
		}
		parent := filepath.Dir(wd)
		if parent == wd {
			t.Fatal("could not find repo root")
		}
		wd = parent
	}
}

func walkGoFiles(t *testing.T, root string, visit func(path string)) {
	t.Helper()
	err := filepath.WalkDir(root, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() {
			switch d.Name() {
			case ".git", "node_modules":
				return filepath.SkipDir
			}
			return nil
		}
		if strings.HasSuffix(path, ".go") {
			visit(path)
		}
		return nil
	})
	if err != nil {
		t.Fatal(err)
	}
}

func parseFile(t *testing.T, path string) *ast.File {
	t.Helper()
	file, err := parser.ParseFile(token.NewFileSet(), path, nil, parser.ImportsOnly)
	if err != nil {
		t.Fatalf("parse %s: %v", path, err)
	}
	return file
}

func slashRel(t *testing.T, root, path string) string {
	t.Helper()
	rel, err := filepath.Rel(root, path)
	if err != nil {
		t.Fatal(err)
	}
	return filepath.ToSlash(rel)
}
